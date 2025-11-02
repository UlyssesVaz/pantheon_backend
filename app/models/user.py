from sqlalchemy import Column, String, Boolean, Integer, ARRAY, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)  # Auth0 user ID
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile
    has_completed_onboarding = Column(Boolean, default=False)
    goals = Column(ARRAY(String), default=list)
    activity_level = Column(String, default="moderate")
    body_weight = Column(Float, nullable=True)
    primary_diet_type = Column(String, nullable=True)
    food_exclusions = Column(ARRAY(String), default=list)
    budget = Column(String, nullable=True)
    meal_layout = Column(String, default="breakfast-lunch-dinner")
    preferred_cooking_days = Column(ARRAY(String), default=list)
    typical_prep_time = Column(Integer, default=30)
    
    # Relationships
    pantry_items = relationship("PantryItem", back_populates="user", cascade="all, delete-orphan")
    week_plans = relationship("WeekPlan", back_populates="user", cascade="all, delete-orphan")
    telemetry_events = relationship("TelemetryEvent", back_populates="user", cascade="all, delete-orphan")