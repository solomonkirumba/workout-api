# app/routes/workouts.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.workout import Workout
from app.models.workout_exercise import WorkoutExercise
from app.schemas.schemas import WorkoutSchema, WorkoutExerciseSchema

workouts_bp = Blueprint('workouts', __name__)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

# GET all workouts
@workouts_bp.route('/', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

# GET single workout by id
@workouts_bp.route('/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout)), 200

# GET exercises in a workout
@workouts_bp.route('/<int:id>/exercises', methods=['GET'])
def get_workout_exercises(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    workout_exercises = WorkoutExercise.query.filter_by(workout_id=id).all()
    result = []
    for we in workout_exercises:
        result.append({
            'id': we.id,
            'exercise': we.exercise.to_dict() if we.exercise else None,
            'sets': we.sets,
            'reps': we.reps,
            'duration': we.duration
        })
    return jsonify(result), 200

# POST create workout
@workouts_bp.route('/', methods=['POST'])
def create_workout():
    data = request.get_json()
    
    # Schema validation
    errors = workout_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Check if workout with same name exists
    existing = Workout.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Workout with this name already exists'}), 400
    
    workout = Workout(name=data['name'])
    db.session.add(workout)
    db.session.commit()
    
    return jsonify(workout_schema.dump(workout)), 201

# POST add exercise to workout
@workouts_bp.route('/<int:id>/exercises', methods=['POST'])
def add_exercise_to_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    data = request.get_json()
    data['workout_id'] = id
    
    # Schema validation
    errors = workout_exercise_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Check if exercise already in workout (optional, preventing duplicates)
    existing = WorkoutExercise.query.filter_by(workout_id=id, exercise_id=data['exercise_id']).first()
    if existing:
        return jsonify({'error': 'Exercise already in workout'}), 400
    
    workout_exercise = WorkoutExercise(
        workout_id=id,
        exercise_id=data['exercise_id'],
        sets=data.get('sets'),
        reps=data.get('reps'),
        duration=data.get('duration')
    )
    db.session.add(workout_exercise)
    db.session.commit()
    
    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

# DELETE workout
@workouts_bp.route('/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    db.session.delete(workout)
    db.session.commit()
    
    return jsonify({'message': 'Workout deleted successfully'}), 200