from pydantic import BaseModel, Field
import uuid


class ApproveRequest(BaseModel):
    affiliate_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    campaign_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    request_sent: bool = False
    approval_status: bool = False