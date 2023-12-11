from fastapi import APIRouter, HTTPException, Request, status
from app.database import (
    click_db,
    transaction_db,
    campaign_db,
    affiliate_db,
)

from app.schemas.campaign import CampaignResponse
from app.schemas.transaction import TransactionBase
from app.utils_internal.misc import jsonToBson

from typing import Dict
from datetime import datetime

from app.config import settings

router: APIRouter = APIRouter(prefix="/postback", tags=["Postback"])


async def get_amount_increment(affiliate_id: str):
    affiliate_data = await affiliate_db.find_one(
        {"affiliate_id": affiliate_id}, {"level": 1, "_id": 0}
    )
    return settings.level_to_increment[affiliate_data.get("level", "silver")]


async def initiate_payouts(data: dict, campaign_id: str, affiliate_id: str):
    event_id: str = data.get("event_id").lower()

    if not affiliate_id or not event_id:
        return

    res = await campaign_db.find_one({"_id": jsonToBson(campaign_id)})

    if not res:
        return
    campaign = CampaignResponse(**res)

    if event_id not in campaign.payouts:
        return

    inc = await get_amount_increment(affiliate_id)

    transaction: TransactionBase = TransactionBase(
        affiliate_id=affiliate_id,
        campaign_id=campaign_id,
        event=event_id,
        amount=campaign.payouts[event_id] * (1 + inc / 100),
    )
    await transaction_db.insert_one(transaction.dict())


@router.get("/")
async def postback(
    request: Request, campaign_id: str, event_id: str = "none", click_id: str = ""
) -> bool:
    affiliate_id: str = ""
    if click_id:
        res = await click_db.find_one(
            {"click_id": click_id, "campaign_id": campaign_id}
        )
        affiliate_id = res["affiliate_id"]
        if not res:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="No such click found."
            )

    data: Dict = request.query_params._dict
    data["time"] = datetime.utcnow()

    await initiate_payouts(data, campaign_id, affiliate_id)

    res = await click_db.update_one(
        {"click_id": click_id},
        {"$push": {"postback_params": data}},
    )

    return res.modified_count > 0
