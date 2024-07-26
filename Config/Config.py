# from pydantic import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_port: str
    postgres_ipaddress: str
    postgres_db_name: str
    
    pgadmin_default_email:str
    pgadmin_default_password:str
    
    secret_key: str
    ALGORITHM: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file="Config/.env", env_file_encoding='utf-8')



settings = Settings()

