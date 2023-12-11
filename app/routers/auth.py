from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.auth import Token
from app import utils, oauth2
from app.oauth2 import OAuth2ResetPasswordRequestForm
from app.schemas.manager import (
    ManagerOut
 
)
from app.constants.email_templates import (
    EMAIL_RESET_PASSWORD_MAIL,
    EMAIL_RESET_PASSWORD_SUBJECT,
)
from app.config import settings
from app.database import affiliate_db,RedisClient,manager_db
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags=["Authentication"])


@router.post("/api/login", response_model=Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
    manager = await manager_db.find_one({"email": credentials.username})
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify(credentials.password, manager["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(
        data={"user_id": manager["manager_id"]}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/reset-password/request")
async def reset_password_request(credentials: OAuth2ResetPasswordRequestForm = Depends(),current_adivitisor: str = Depends(oauth2.get_current_user))-> JSONResponse:
    manager_password = await manager_db.find_one({"email": credentials.username})
    if not manager_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Username"
        )

    reset_token = oauth2.create_access_token(
        data={"user_id": manager_password["manager_id"]}
    )
    
    res = await manager_db.find_one({"manager_id": current_adivitisor})
    manager = ManagerOut(**res)
    code = utils.gen_code()
    print(code)
    await RedisClient.set("emailcode_" + manager.affiliate_id, code, exp=5 * 60)
    utils.send_email(
        reciever=manager.email,
        subject=EMAIL_RESET_PASSWORD_SUBJECT,
        html=EMAIL_RESET_PASSWORD_MAIL
        % (
            manager.name,
            settings.reset_password_url
            + f"/api/misc/reset_password/request?affiliate_id={manager.manager_id}&code={code}",
        ),
    )
    return JSONResponse(
        {"message": "Reset Password Mail Sent, link will expire in 5 minutes."},
        status_code=status.HTTP_200_OK,
    )


