from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_url: str
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = ".env"


settings = Settings()
