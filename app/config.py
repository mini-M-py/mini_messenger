from pydantic import BaseSettings

class Setting(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    email: str
    password: str
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    class Config:
        env_file = ".env"

setting = Setting()