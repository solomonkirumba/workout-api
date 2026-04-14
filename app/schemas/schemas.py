# app/schemas/schemas.py
from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.workout_exercise import WorkoutExercise

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    created_at = fields.DateTime(dump_only=True)
    
    # Schema validation
    @validates('name')
    def validate_name(self, value):
        if not value or value.strip() == '':
            raise ValidationError("Workout name cannot be empty")
        if len(value) > 100:
            raise ValidationError("Workout name must be less than 100 characters")

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    muscle_group = fields.Str(required=True, validate=validate.OneOf(['Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core']))
    description = fields.Str(allow_none=True)
    
    @validates('name')
    def validate_name(self, value):
        if not value or value.strip() == '':
            raise ValidationError("Exercise name cannot be empty")

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration = fields.Int(allow_none=True, validate=validate.Range(min=1))
    
    # Schema validation: at least one of sets, reps, or duration must be provided
    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be greater than 0")
    
    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be greater than 0")
    
    @validates('duration')
    def validate_duration(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration must be greater than 0")
    
    @validates('workout_id')
    def validate_workout_id(self, value):
        from app.models.workout import Workout
        workout = Workout.query.get(value)
        if not workout:
            raise ValidationError(f"Workout with id {value} does not exist")
    
    @validates('exercise_id')
    def validate_exercise_id(self, value):
        from app.models.exercise import Exercise
        exercise = Exercise.query.get(value)
        if not exercise:
            raise ValidationError(f"Exercise with id {value} does not exist")