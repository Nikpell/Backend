
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bd_url: SecretStr
    jwt_secret: SecretStr
    transaction_private_key: SecretStr
    secret_key: SecretStr
    algorithm: SecretStr
    signature: SecretStr
    inspiration_delta: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
