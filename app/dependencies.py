from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth0 import verify_token # Your "Gatekeeper"
from app.models.user import User

async def get_current_user(
    token_payload: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> User:
    """
    Get or create current user from database based on Auth0 token.
    This runs on almost every authenticated endpoint.
    """
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID (sub) not found in token"
        )
        
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        # User's first login. Create them in our DB.
        email = token_payload.get("email")
        
        user = User(
            id=user_id, # Use Auth0 'sub' as our primary key
            email=email
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user