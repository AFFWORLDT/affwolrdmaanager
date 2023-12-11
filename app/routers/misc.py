from fastapi import HTTPException, status, APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from app.database import affiliate_db, RedisClient
from app.schemas.manager import ManagerDB
from app.utils_internal import campaign_utils
from app.config import settings
from app.constants.iframe import IFRAME_SRC
from app.utils import hash

router = APIRouter(prefix="/api/misc", tags=["Misc"])


@router.get("/iframe_redirect")
async def iframe_redirect(affiliate_id: str):
    affiliate = await affiliate_db.find_one({"affiliate_id": affiliate_id})
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Affiliate not found."
        )
    affiliate = ManagerDB(**affiliate)
    campaign = await campaign_utils.get_campaign(
        affiliate.iframe_campaign_id, {"code": 1, "_id": 0}
    )
    return RedirectResponse(settings.admin_api_url + "/{}".format(campaign["code"]))


@router.get("/iframe_code")
async def iframe_code(affiliate_id: str):
    affiliate = await affiliate_db.find_one({"affiliate_id": affiliate_id})
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Affiliate not found."
        )
    affiliate = ManagerDB(**affiliate)
    campaign = await campaign_utils.get_campaign(
        affiliate.iframe_campaign_id, {"image_url": 1, "_id": 0, "code": 1}
    )
    return HTMLResponse(
        IFRAME_SRC.format(
            settings.admin_api_url + "/" + campaign["code"], campaign["image_url"]
        )
    )


@router.get("/verify_email")
async def verify_email(affiliate_id: str, code: str):
    code_from_redis = await RedisClient.get("emailcode_" + affiliate_id)
    if code_from_redis.decode() != code:
        return HTMLResponse("<h2>Code did'nt matched or link expired, try again</h2>")
    await affiliate_db.update_one(
        {"affiliate_id": affiliate_id}, {"$set": {"verified": True}}
    )

    return HTMLResponse("<h2>Email Verified, you may close this window.</h2>")

@router.get("/reset_password/request")
async def reset_password_email(affiliate_id: str, code: str):
    print(f"Received request for reset_password_email with affiliate_id: {affiliate_id}, code: {code}")
    code_from_redis_bytes = await RedisClient.get("emailcode_" + affiliate_id)
    code_from_redis = code_from_redis_bytes.decode('utf-8') if code_from_redis_bytes else None
    print("code_from_redis__",code_from_redis)
    print("code__",code)
    if code_from_redis != code:
        return HTMLResponse("<h2>Code didn't match or link expired, try again</h2>")

    return HTMLResponse(
        """
        <form method="post" action="/reset_password/process">
            <input type="hidden" name="affiliate_id" value="{}">
            <input type="hidden" name="code" value="{}">
            <label for="new_password">New Password:</label>
            <input type="password" id="new_password" name="new_password" required>
            <br>
            <label for="confirm_password">Confirm Password:</label>
            <input type="password" id="confirm_password" name="confirm_password" required>
            <br>
            <button type="submit">Reset Password</button>
        </form>
        """.format(affiliate_id, code)
    )


@router.post("/reset_password/process")
async def reset_password_process(
    affiliate_id: str, code: str, new_password: str, confirm_password: str
):
    code_from_redis = await RedisClient.get("emailcode_" + affiliate_id)
    if code_from_redis.decode() != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code didn't match or link expired, try again",
        )

    if new_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    # Update the affiliate's password in the database
    hashed_password = hash(new_password)
    await affiliate_db.update_one(
        {"affiliate_id": affiliate_id}, {"$set": {"password": hashed_password}}
    )

    return HTMLResponse("<h2>Password successfully reset</h2>")