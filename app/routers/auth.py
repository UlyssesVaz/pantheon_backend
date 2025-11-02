from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserProfileUpdate, UserResponse
from app.dependencies import get_current_user
from app.utils.auth0_management import update_auth0_app_metadata

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's full profile from *our* database.
    This is called by the frontend on every app load after login.
    """
    return current_user

@router.post("/complete-onboarding", response_model=UserResponse)
async def complete_onboarding(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    The main onboarding endpoint from the frontend.
    1. Saves the full profile to *our* database.
    2. Pushes *only* the 'hasCompletedOnboarding' flag to Auth0 app_metadata.
    """
    
    # 1. Update our local database with the full profile
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.has_completed_onboarding = True
        
    db.commit()
    db.refresh(current_user)

    # 2. Update Auth0 app_metadata with ONLY the flag.
    # This is what your frontend's useEffect hook will check on next login.
    try:
        await update_auth0_app_metadata(current_user.id, {
            "hasCompletedOnboarding": True,
        })
    except Exception as e:
        # This is not a fatal error, but we should log it.
        # The user's profile is saved in our DB, which is the source of truth.
        print(f"Warning: Failed to update Auth0 metadata for {current_user.id}. Error: {e}")
        
    return current_user

@router.put("", response_model=UserResponse)
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