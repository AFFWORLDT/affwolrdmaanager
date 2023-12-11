from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.obj import PyObjectId
from bson import ObjectId
from typing import List, Optional


class TransactionBase(BaseModel):
    affiliate_id: str
    campaign_id: str
    event: str = ""
    amount: float
    approved: bool = False
    initiated_at: datetime


class TransactionResponse(TransactionBase):
    transaction_id: PyObjectId = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class Postback(BaseModel):
    event_id: str
    time: datetime


class Click(BaseModel):
    click_id: str
    campaign_id: str
    client_addr: str
    postback_params: List[Postback] = []
    timestamp: datetime = None


class DataFilter(BaseModel):
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    campaign: Optional[str]
    page: int = 1
