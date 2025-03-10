from pydantic_settings import BaseSettings
from pydantic import Field

class Config(BaseSettings):
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    db_name: str = Field(default="", env="DB_NAME")
    db_user: str = Field(default="", env="DB_USER")
    db_password: str = Field(default="", env="DB_PASSWORD")
    db_host: str = Field(default="", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")

    class Config:
        env_file = ".venv"

config = Config()