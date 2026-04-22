from flask import Blueprint, request, jsonify
from app import db
from app.models.workout import Workout
from app.models.workout_exercise import WorkoutExercise
from app.schemas.schemas import WorkoutSchema, WorkoutExerciseSchema

workouts_bp = Blueprint('workouts', __name__)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

# GET all workouts (with pagination)
@workouts_bp.route('/', methods=['GET'])
def get_workouts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 50)
    
    paginated = Workout.query.order_by(Workout.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'workouts': workouts_schema.dump(paginated.items),
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'pages': paginated.pages,
        'has_next': paginated.has_next,
        'has_prev': paginated.has_prev
    }), 200

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
    
    errors = workout_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
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
    
    errors = workout_exercise_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
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