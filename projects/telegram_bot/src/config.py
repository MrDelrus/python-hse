from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Config(BaseSettings):
    env: str
    bot_token: SecretStr

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )


settings = Config()
