# app/models/exercise.py
from app import db

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    muscle_group = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    
    # Table constraints
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_exercise_name'),
        db.CheckConstraint("muscle_group IN ('Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core')", name='chk_muscle_group'),
    )
    
    # Relationship to WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    
    # Model validations
    @db.validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Exercise name cannot be empty")
        if len(name) > 100:
            raise ValueError("Exercise name must be less than 100 characters")
        return name.strip()
    
    @db.validates('muscle_group')
    def validate_muscle_group(self, key, muscle_group):
        valid_groups = ['Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core']
        if muscle_group not in valid_groups:
            raise ValueError(f"Muscle group must be one of: {valid_groups}")
        return muscle_group
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'muscle_group': self.muscle_group,
            'description': self.description
        }