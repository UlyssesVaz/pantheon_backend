from sqlalchemy import Column, String, Integer, JSON, ARRAY, DateTime
from datetime import datetime
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cook_time = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    ingredients = Column(JSON, nullable=False)  # Array of ingredient objects
    main_ingredients = Column(ARRAY(String), nullable=False)
    instructions = Column(JSON, nullable=False)  # Array of step strings
    tags = Column(ARRAY(String), default=list)
    cuisine = Column(String, nullable=True)
    prep_complexity = Column(String, nullable=False)  # quick, prep
    
    # Meal framework
    protein = Column(String, nullable=True)
    grain = Column(String, nullable=True)
    vegetable = Column(String, nullable=True)
    
    # Metadata
    image_url = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=True)  # user_id or "system"