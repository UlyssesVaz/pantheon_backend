from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class PantryItem(Base):
    __tablename__ = "pantry_items"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    category = Column(String, nullable=False)  # protein, grain, vegetable, etc.
    storage_location = Column(String, nullable=False)  # pantry, fridge, freezer
    added_at = Column(DateTime, default=datetime.utcnow)
    purchase_source = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="pantry_items")