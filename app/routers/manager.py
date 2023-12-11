from app import utils
from fastapi import HTTPException, status, Depends, APIRouter, UploadFile
from fastapi.responses import JSONResponse
from app.schemas.manager import (
    ManagerCreate,
    ManagerDB,
    ManagerOut
)
from pymongo.collection import ReturnDocument
from app.utils_internal import campaign_utils
from app.database import affiliate_db, manager_db, RedisClient
from app import oauth2, utils
from app.constants.file_upload_consts import MB, SUPPORTED_FILE_TYPES
from app.constants.email_templates import (
    EMAIL_VERIFICATION_MAIL,
    EMAIL_VERIFICATION_SUBJECT,
)
import magic
import asyncio
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor
from app.config import S3, settings

router = APIRouter(prefix="/api/managers", tags=["managers"])




@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_manager(manager: ManagerCreate) -> ManagerOut:
    exists = await manager_db.find_one({"email": manager.email})
    if exists:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="account with that email already exists.",
        )
    new_manager: ManagerDB = ManagerDB(**manager.dict())
    new_manager.password = utils.hash(new_manager.password)
    res = await manager_db.insert_one(new_manager.dict())
    access_token = oauth2.create_access_token(
        data={"user_id": new_manager.manager_id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/")
async def get_info(
    current_manager: str = Depends(oauth2.get_current_user),
) -> ManagerOut:
    manager = await manager_db.find_one({"manager_id": current_manager})
    return ManagerOut(**manager)


