# In: app/utils/auth0_management.py

import httpx
from functools import lru_cache
from app.config import get_settings

settings = get_settings()

@lru_cache(maxsize=1)
def get_auth0_management_token() -> str:
    """
    Get a new Management API token from Auth0.
    This is cached in memory.
    """
    payload = {
        "client_id": settings.auth0_management_client_id,
        "client_secret": settings.auth0_management_client_secret,
        "audience": f"https://{settings.auth0_domain}/api/v2/",
        "grant_type": "client_credentials"
    }
    headers = {'content-type': "application/json"}
    
    try:
        response = httpx.post(f"https://{settings.auth0_domain}/oauth/token", json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses (4xx, 5xx)
        token_data = response.json()
        return token_data["access_token"]
    except httpx.HTTPStatusError as e:
        print(f"Error getting Auth0 Management Token: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

async def update_auth0_app_metadata(user_id: str, metadata: dict) -> bool:
    """
    Updates the app_metadata for a given Auth0 user.
    """
    token = get_auth0_management_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"https://{settings.auth0_domain}/api/v2/users/{user_id}"
    payload = {"app_metadata": metadata}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            print(f"Error updating Auth0 metadata for {user_id}: {e}")
            return False