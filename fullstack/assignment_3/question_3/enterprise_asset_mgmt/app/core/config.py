from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./enterprise_asset.db"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
