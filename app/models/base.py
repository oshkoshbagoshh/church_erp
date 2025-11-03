"""Base model module."""
from datetime import datetime
from ..extensions import db

class BaseModel(db.Model):
    """Base model class that includes common fields and methods."""
    
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save the model instance."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the model instance."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        """Get a record by ID."""
        return cls.query.get(id)