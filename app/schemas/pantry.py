from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PantryItemBase(BaseModel):
    name: str
    quantity: float
    unit: str
    expires_at: Optional[datetime] = None
    category: str
    storage_location: str
    purchase_source: Optional[str] = None

class PantryItemCreate(PantryItemBase):
    pass

class PantryItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    expires_at: Optional[datetime] = None
    category: Optional[str] = None
    storage_location: Optional[str] = None

class PantryItemResponse(PantryItemBase):
    id: str
    user_id: str
    added_at: datetime
    
    class Config:
        from_attributes = True