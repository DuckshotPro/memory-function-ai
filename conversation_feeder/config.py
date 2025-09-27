from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str
    database_url: str
    feeder_auth_token: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
