from fastapi import FastAPI
from app.routers import auth, manager, misc, campaign,postback,analytics
from fastapi.middleware.cors import CORSMiddleware
from app.database import RedisClient
from app.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def connect_redis():
    await RedisClient.connect_redis(settings.redis_url)


app.include_router(manager.router)
app.include_router(auth.router)
app.include_router(misc.router)
app.include_router(campaign.router)
app.include_router(postback.router)
app.include_router(analytics.router)


@app.get("/")
def home():
    return {"message": " /docs for documentation "}
