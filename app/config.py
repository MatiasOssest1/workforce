from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_url: str
    database_schema: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'


settings = Settings()