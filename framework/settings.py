from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "dev"

    class Config:
        env_file = ".env"


settings = Settings()
