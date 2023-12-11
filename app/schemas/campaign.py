from app.schemas.obj import PyObjectId

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any
from bson import ObjectId
from datetime import datetime
from enum import Enum


class CampaignStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    PAUSED = "paused"
       
class CampaignCountry(str, Enum):
    INDIA = "India"
    AUSTRALIA = "Australia"
    CANADA = "Canada"
    BRAZIL = "Brazil"
    VIETNAM = "Vietnam"
    RUSSIA = "Russia"   

class CampaignCategory(str, Enum):
    ECOMMERCE = "Ecommerce"
    BFSI = "BFSI"
    BANKING = "Banking"
    CASINO = "Casino"
    CPL = "CPL"
    CPR = "CPR"
    CPD = "CPD"
    CPS = "CPS"
    GAMBLING = "Gambling"
    CRYPTO = "Crypto"
    SURVEY = "Survey"

class CampaignType(str, Enum):
    PRIVATE = "Private"
    PUBLIC = "Public"
    
class CampaignRequest(BaseModel):
    name: str
    category: Optional[CampaignCategory] = None
    country : Optional[CampaignCountry] = None
    Tags: Optional[List[str]] = []
    description: Optional[str] = ""
    url: HttpUrl
    payouts: Dict[str, float] = {}
    image_url: str = ""
    status: CampaignStatus = CampaignStatus.ACTIVE
    type: Optional[CampaignType] = None

class UpdateCampaignRequest(BaseModel):
    campaign_id: str
    name: str
    CampaignPhoto: Optional[str]=""
    description: Optional[str] = ""
    payouts: Dict[str, float] = {}
    image_url: str = ""
    status: CampaignStatus = CampaignStatus.ACTIVE


class CampaignResponse(CampaignRequest):
    campaign_id: PyObjectId = Field(alias="_id")
    code: str

    class Config:
        json_encoders = {ObjectId: str}


class CampaignResult(BaseModel):
    campaign_id: PyObjectId
    redirect: HttpUrl

    class Config:
        json_encoders = {ObjectId: str}


class ClickBase(BaseModel):
    click_id: str
    campaign_id: str
    client_addr: str
    affiliate_id: str = ""
    postback_params: List[Dict[str, Any]] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())
