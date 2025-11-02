from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "Athyra API"
    debug: bool = True
    
    # Database
    database_url: str
    
    # Auth0
    auth0_domain: str
    auth0_api_audience: str
    auth0_algorithms: list[str] = ["RS256"]
    auth0_management_client_id: str
    auth0_management_client_secret: str
    
    # AI
    anthropic_api_key: str
    openai_api_key: str = ""
    
    # Email
    sendgrid_api_key: str
    from_email: str
    
    # Frontend
    frontend_url: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()