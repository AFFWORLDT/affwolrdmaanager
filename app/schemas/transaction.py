from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.obj import PyObjectId
from bson import ObjectId


class TransactionBase(BaseModel):
    affiliate_id: str
    campaign_id: str
    event: str = ""
    amount: float
    approved: bool = False
    initiated_at: datetime = Field(default_factory=lambda: datetime.utcnow())


class TransactionResponse(TransactionBase):
    transaction_id: PyObjectId = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
