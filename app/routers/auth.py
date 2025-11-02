# In: app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserProfileUpdate, UserResponse
from app.dependencies import get_current_user
from app.utils.auth0_management import update_auth0_app_metadata

router = APIRouter(tags=["profile"])

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's profile from *our* database.
    This is called by the frontend on load to get profile data.
    """
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's profile in *our* database.
    This is for all future profile updates (from the settings page).
    """
    update_data = profile_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
        
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.post("/complete-onboarding", response_model=UserResponse)
async def complete_onboarding(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    The main onboarding endpoint.
    1. Saves the full profile to *our* database.
    2. Pushes the 'hasCompletedOnboarding' flag to Auth0 app_metadata.
    """
    
    # 1. Update our local database with the full profile
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    # Ensure onboarding is marked as true
    current_user.has_completed_onboarding = True
        
    db.commit()
    db.refresh(current_user)

    # 2. Update Auth0 app_metadata with ONLY the flag
    auth0_metadata = {"hasCompletedOnboarding": True}
    success = await update_auth0_app_metadata(current_user.id, auth0_metadata)
    
    if not success:
        # This isn't a fatal error, but we should know about it.
        # The user can continue, but might see onboarding again on next login.
        print(f"Warning: Failed to update Auth0 metadata for {current_user.id}")
        
    return current_user