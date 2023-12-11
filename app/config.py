from pydantic import BaseSettings
import boto3


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    mongo_uri: str
    access_token_expire_minutes: int

    db_name: str

    affilator_base_db: str = "affilator"
    admin_api_url: str = ""

    base_url: str = "https://affiliate-api.affworld.cloud"

    reset_password_url: str = "https://affiliate-api.affworld.cloud"

    aws_access_key: str

    affworld_bucket: str = "affworld-bucket"

    redis_url: str

    aws_secret_access_key: str

    class Config:
        env_file = ".env"


settings = Settings()


S3 = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key,
    aws_secret_access_key=settings.aws_secret_access_key,
)
