from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database.db import Base
from models.base import BaseModel

class Category(Base, BaseModel):
    """Category model for organizing tasks."""
    
    __tablename__ = 'categories'
    
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(7), default="#007BFF")  # Hex color code with default blue
    
    # Relationship to tasks
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category {self.name}>"


class Task(Base, BaseModel):
    """Task model for to-do items."""
    
    __tablename__ = 'tasks'
    
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=2)  # 1=Low, 2=Medium, 3=High
    completed = Column(Boolean, default=False)
    
    # Foreign key to Category
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship("Category", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task {self.title}>"
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and not self.completed:
            return datetime.now() > self.due_date
        return False
    
    @property
    def priority_label(self):
        """Return a text representation of priority."""
        priority_map = {1: "Low", 2: "Medium", 3: "High"}
        return priority_map.get(self.priority, "Medium")
