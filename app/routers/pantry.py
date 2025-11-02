from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import uuid

from app.database import get_db
from app.models.user import User
from app.models.pantry import PantryItem
from app.schemas.pantry import PantryItemCreate, PantryItemUpdate, PantryItemResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/pantry", tags=["pantry"])

@router.get("/", response_model=List[PantryItemResponse])
async def get_pantry_items(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all pantry items for current user"""
    items = db.query(PantryItem).filter(
        PantryItem.user_id == current_user.id
    ).order_by(PantryItem.added_at.desc()).all()
    
    return items

@router.get("/{item_id}", response_model=PantryItemResponse)
async def get_pantry_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific pantry item"""
    item = db.query(PantryItem).filter(
        PantryItem.id == item_id,
        PantryItem.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item

@router.post("/", response_model=PantryItemResponse, status_code=status.HTTP_201_CREATED)
async def create_pantry_item(
    item: PantryItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new pantry item"""
    db_item = PantryItem(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        **item.model_dump()
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

@router.put("/{item_id}", response_model=PantryItemResponse)
async def update_pantry_item(
    item_id: str,
    item_update: PantryItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a pantry item"""
    db_item = db.query(PantryItem).filter(
        PantryItem.id == item_id,
        PantryItem.user_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pantry_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a pantry item"""
    db_item = db.query(PantryItem).filter(
        PantryItem.id == item_id,
        PantryItem.user_id == current_user.id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()

@router.get("/expiring", response_model=List[PantryItemResponse])
async def get_expiring_items(
    days: int = 3,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get items expiring within specified days"""
    expiring_date = datetime.utcnow() + timedelta(days=days)
    
    items = db.query(PantryItem).filter(
        PantryItem.user_id == current_user.id,
        PantryItem.expires_at <= expiring_date,
        PantryItem.expires_at >= datetime.utcnow(),
        PantryItem.storage_location != "freezer"
    ).order_by(PantryItem.expires_at).all()
    
    return items

@router.post("/clear-expiring", status_code=status.HTTP_204_NO_CONTENT)
async def clear_expiring_items(
    days: int = 3,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete items expiring within specified days"""
    expiring_date = datetime.utcnow() + timedelta(days=days)
    
    db.query(PantryItem).filter(
        PantryItem.user_id == current_user.id,
        PantryItem.expires_at <= expiring_date,
        PantryItem.expires_at >= datetime.utcnow(),
        PantryItem.storage_location != "freezer"
    ).delete()
    
    db.commit()