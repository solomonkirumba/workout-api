# app/schemas/schemas.py
from marshmallow import Schema, fields, validate, ValidationError
from app.models.workout_exercise import WorkoutExercise

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100, error="Workout name must be between 1 and 100 characters")
    )
    created_at = fields.DateTime(dump_only=True)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="Exercise name must be between 1 and 100 characters")
    )
    muscle_group = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core'],
            error="Muscle group must be one of: Chest, Back, Legs, Shoulders, Arms, Core"
        )
    )
    description = fields.Str(allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1, error="Sets must be greater than 0"))
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1, error="Reps must be greater than 0"))
    duration = fields.Int(allow_none=True, validate=validate.Range(min=1, error="Duration must be greater than 0"))
    
    # Custom validation: at least one of sets, reps, or duration must be provided
    @staticmethod
    def validate_sets_reps_duration(data, **kwargs):
        sets = data.get('sets')
        reps = data.get('reps')
        duration = data.get('duration')
        
        if not sets and not reps and not duration:
            raise ValidationError("At least one of sets, reps, or duration must be provided")
        return data
    
    # Foreign key existence validation
    @staticmethod
    def validate_workout_id(data, **kwargs):
        from app.models.workout import Workout
        workout = Workout.query.get(data.get('workout_id'))
        if not workout:
            raise ValidationError(f"Workout with id {data.get('workout_id')} does not exist")
        return data
    
    @staticmethod
    def validate_exercise_id(data, **kwargs):
        from app.models.exercise import Exercise
        exercise = Exercise.query.get(data.get('exercise_id'))
        if not exercise:
            raise ValidationError(f"Exercise with id {data.get('exercise_id')} does not exist")
        return data