from fastapi import APIRouter, Depends
from app.schemas.campaign import (
    UpdateCampaignRequest,
    CampaignRequest,
    CampaignResponse,
    CampaignResult,
    ClickBase,
    CampaignStatus,
)
from app.database import (
    campaign_db,
    click_db,
    affiliate_db,
    advitisor_db,
)
from app.utils_internal import campaign_utils
from app.utils_internal.misc import bsonToJson, jsonToBson
from app.config import settings
from app.schemas.campaign import CampaignResponse

from fastapi import HTTPException, BackgroundTasks, status
from starlette.responses import RedirectResponse
from app import oauth2

import uuid
from typing import Optional, List, Dict
from bson.errors import InvalidId
from datetime import datetime

router: APIRouter = APIRouter(prefix="/campaign", tags=["Campaign"])


@router.post("/")
async def create_campaign(
    payload: CampaignRequest,current_advitisor: str = Depends(oauth2.get_current_user),
) -> CampaignResult:
    
    res = await advitisor_db.find_one({"advitisor_id": current_advitisor}, {"_id": 1})
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="advitisor id not found"
        )

    data: dict = payload.dict()
    data["advitisor_id"] = current_advitisor
    data["code"] = await campaign_utils.get_short_code()
    res = await campaign_db.insert_one(data)
    if res.inserted_id:
        res = await campaign_db.find_one({"code": data["code"]})
        return CampaignResult(
            redirect=settings.base_url + "/" + data["code"], campaign_id=res["_id"]
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="an error occured !"
    )


@router.put("/")
async def update_campaign(
    payload: UpdateCampaignRequest
) -> bool:
    campaign = await campaign_db.find_one({"_id": jsonToBson(payload.campaign_id)})
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such campaign found."
        )
    update_result = await campaign_db.update_one(
        {"_id": jsonToBson(payload.campaign_id)},
        {
            "$set": {
                "name": payload.name,
                "image_url": payload.image_url,
                "description": payload.description,
                "payouts": payload.payouts,
            }
        },
    )
    return update_result.modified_count > 0

@router.get("/")
async def get_campaigns(current_advitisor: str = Depends(oauth2.get_current_user),page: int = 1, status: str = ""):
    skip = (page - 1) * 30

    campaigns = (
        campaign_db.find({"advitisor_id": current_advitisor} if not status else {"advitisor_id": current_advitisor, "status": status})
        .skip(skip)
        .limit(30)
    )
    return [CampaignResponse(**c) async for c in campaigns]



@router.get("/clicks")
async def get_clicks(
    campaign_id: str,start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[ClickBase]:
    query = {"campaign_id": campaign_id}
    
    if start_date and end_date:
        print("Start Date:", start_date)
        print("End Date:", end_date)
        query["timestamp"] = {"$gte": start_date, "$lte": end_date}
    print("Query:", query)
    res = click_db.find(query)
    print("RES:",res)
    return [ClickBase(**click) async for click in res]



@router.get("/{campaign_id}")
async def get_campaign(campaign_id: str) -> CampaignResponse:
    res = await campaign_db.find_one({"_id": jsonToBson(campaign_id)})
    return CampaignResponse(**res)


@router.delete("/{id}")
async def delete_campaign(
    id: str,
) -> dict:
    await click_db.delete_many({"campaign_id": id})
    await campaign_db.delete_one({"_id": jsonToBson(id)})
    return {"message": "success"}
