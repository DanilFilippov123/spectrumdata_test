from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "dev"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
