from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from database.db import Base

class BaseModel(object):
    """Base model class that includes common columns and methods."""
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def as_dict(self):
        """Return the model as a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def get_by_id(cls, id):
        """Get a record by ID."""
        return cls.query.filter(cls.id == id).first()
    
    @classmethod
    def get_all(cls):
        """Get all records."""
        return cls.query.all()
    
    def save(self, session):
        """Save the record to the database."""
        session.add(self)
        session.commit()
    
    def delete(self, session):
        """Delete the record from the database."""
        session.delete(self)
        session.commit()
