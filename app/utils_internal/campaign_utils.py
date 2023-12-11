from fastapi import HTTPException, status
from app.database import campaign_db
from bson import ObjectId

from app.schemas.campaign import CampaignResponse

from uuid import uuid4


async def get_campaign(campaign_id: str, get_cols: dict = {}):
    if ObjectId.is_valid(oid=campaign_id):
        campaign = await campaign_db.find_one(
            {"_id": ObjectId(oid=campaign_id)}, get_cols
        )
        if campaign:
            return campaign
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
    )

async def get_short_code() -> str:
    code: str = uuid4().hex[:6]
    res = await campaign_db.find_one({"code": code})
    while res:
        code: str = uuid4().hex[:6]
        res = await campaign_db.find_one({"code": code})
    return code


async def get_campaign_or_404(filter: dict = {}) -> CampaignResponse:
    campaign = await campaign_db.find_one(filter)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no such campaign available"
        )
    return CampaignResponse(**campaign)