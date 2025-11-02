from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth0 import get_current_user_id
from app.models.user import User

async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> User:
    """Get or create current user from database"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        # Create user if doesn't exist (first login)
        user = User(id=user_id, email=user_id)  # Auth0 sub as ID
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user