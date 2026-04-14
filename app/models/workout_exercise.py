# app/models/workout_exercise.py
from app import db

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration = db.Column(db.Integer)  # in seconds
    
    # Table constraints: at least one of sets/reps/duration must be present
    __table_args__ = (
        db.CheckConstraint(
            '(sets IS NOT NULL AND sets > 0) OR (reps IS NOT NULL AND reps > 0) OR (duration IS NOT NULL AND duration > 0)',
            name='chk_exercise_detail'
        ),
    )
    
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    # Model validations
    @db.validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets <= 0:
            raise ValueError("Sets must be greater than 0")
        return sets
    
    @db.validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError("Reps must be greater than 0")
        return reps
    
    @db.validates('duration')
    def validate_duration(self, key, duration):
        if duration is not None and duration <= 0:
            raise ValueError("Duration must be greater than 0")
        return duration
    
    def to_dict(self):
        return {
            'id': self.id,
            'workout_id': self.workout_id,
            'exercise': self.exercise.to_dict() if self.exercise else None,
            'sets': self.sets,
            'reps': self.reps,
            'duration': self.duration
        }