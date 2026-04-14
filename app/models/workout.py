# app/models/workout.py
from app import db
from datetime import datetime

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Table constraint: name must be unique
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_workout_name'),
    )
    
    # Relationship to WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    
    # Model validation
    @db.validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Workout name cannot be empty")
        if len(name) > 100:
            raise ValueError("Workout name must be less than 100 characters")
        return name.strip()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }