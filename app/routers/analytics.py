from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from app.database import click_db, transactions_db
from app import oauth2
from app.schemas.misc import TransactionResponse, Click, DataFilter
from typing import List

from bson import ObjectId

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/clicks")
async def get_offer_clicks(
    current_affiliate: str = Depends(oauth2.get_current_user),
) -> JSONResponse:
    pipeline = [
        {"$match": {"affiliate_id": current_affiliate}},
        {
            "$lookup": {
                "from": "campaign",
                "let": {"campaign_id_str": "$campaign_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$_id", {"$toObjectId": "$$campaign_id_str"}]
                            }
                        }
                    }
                ],
                "as": "campaign",
            }
        },
        {"$unwind": "$campaign"},
        {
            "$group": {
                "_id": "$campaign_id",
                "name": {"$first": "$campaign.name"},
                "url": {"$first": "$campaign.url"},
                "code": {"$first": "$campaign.code"},
                "description": {"$first": "$campaign.description"},
                "count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "campaign_id": "$_id",
                "url": 1,
                "name": 1,
                "count": 1,
            }
        },
    ]
    res = await click_db.aggregate(pipeline).to_list(None)
    return JSONResponse(content=res)

