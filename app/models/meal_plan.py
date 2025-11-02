from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class WeekPlan(Base):
    __tablename__ = "week_plans"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    week_of = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    shared_ingredients = Column(ARRAY(String), default=list)
    
    # Relationships
    user = relationship("User", back_populates="week_plans")
    meals = relationship("MealPlan", back_populates="week_plan", cascade="all, delete-orphan")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(String, primary_key=True, index=True)
    week_plan_id = Column(String, ForeignKey("week_plans.id"), nullable=False)
    recipe_id = Column(String, ForeignKey("recipes.id"), nullable=False)
    day = Column(String, nullable=False)  # Monday, Tuesday, etc.
    meal_type = Column(String, nullable=False)  # breakfast, lunch, dinner
    
    # Relationships
    week_plan = relationship("WeekPlan", back_populates="meals")