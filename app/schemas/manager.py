from pydantic import BaseModel, EmailStr, Field, root_validator
from datetime import datetime
from typing import Optional, Union, List
from enum import Enum

import uuid


class AdvitisorCategory(str, Enum):
    ECOMMERCE = "ecommerce"
    GOLD = "gold"
    DIAMOND = "diamond"
    LEGEND = "legend"

class AdvitisorStatus(str, Enum):
    ACTIVE = "active"
    GOLD = "gold"
    DIAMOND = "diamond"
    LEGEND = "legend"


class ManagerCreate(BaseModel):
    name: str
    manager: str
    email: EmailStr
    password: str


class ManagerDB(ManagerCreate):
    affiliate_id: List[str] = Field(default_factory=lambda: [uuid.uuid4().hex])  # Change the type here to an array of strings
    manager_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())
    number: Union[int, float] = None  # Change the type here to number
    skype: str = ""
    profile_pic: str = ""

class ManagerOut(BaseModel):
    name: str
    manager: str
    manager_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    email: EmailStr
    affiliate_id: List[str] = Field(default_factory=lambda: [uuid.uuid4().hex])  # Change the type here to an array of strings
    number: Union[int, float] = None  # Change the type here to number
    skype: str = ""
    profile_pic: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    

class PaymentDetailsBase(BaseModel):
    account_number: str
    beneficiary_name: str
    beneficiary_address: str
    bank_name: str
    bank_address: str
    sort_code: str
    iban: str
    swift: str
    account_type: str = "current"

    @root_validator(pre=True)
    def valid(cls, v):
        account_type: str = v.get("account_type", "").strip().lower()
        if account_type not in ["current", "saving"]:
            raise ValueError("account_type can only be 'current' or 'saving'")
        return v


class PaymentDetailsDB(PaymentDetailsBase):
    payment_detail_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    affiliate_id: str
