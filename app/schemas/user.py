from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr

class UserProfileUpdate(BaseModel):
    has_completed_onboarding: Optional[bool] = None
    goals: Optional[List[str]] = None
    activity_level: Optional[str] = None
    body_weight: Optional[float] = None
    primary_diet_type: Optional[str] = None
    food_exclusions: Optional[List[str]] = None
    budget: Optional[str] = None
    meal_layout: Optional[str] = None
    preferred_cooking_days: Optional[List[str]] = None
    typical_prep_time: Optional[int] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    has_completed_onboarding: bool
    goals: List[str]
    activity_level: str
    body_weight: Optional[float]
    primary_diet_type: Optional[str]
    food_exclusions: List[str]
    budget: Optional[str]
    meal_layout: str
    preferred_cooking_days: List[str]
    typical_prep_time: int
    
    class Config:
        from_attributes = True