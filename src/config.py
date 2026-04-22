from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration.
    Environment variables should be prefixed with WB_.
    Example: WB_TOKEN_GENERAL, WB_TOKEN_WAREHOUSE
    """
    token_general: Optional[str] = None
    token_warehouse: Optional[str] = None
    token_products: Optional[str] = None
    token_inventory: Optional[str] = None
    token_prices: Optional[str] = None
    token_media: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="WB_")

# Singleton instance
settings = Settings()
