# app/routes/exercises.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.exercise import Exercise
from app.schemas.schemas import ExerciseSchema

exercises_bp = Blueprint('exercises', __name__)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

# GET all exercises
@exercises_bp.route('/', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

# GET single exercise by id
@exercises_bp.route('/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_schema.dump(exercise)), 200

# POST create exercise
@exercises_bp.route('/', methods=['POST'])
def create_exercise():
    data = request.get_json()
    
    # Schema validation
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Check if exercise with same name exists
    existing = Exercise.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Exercise with this name already exists'}), 400
    
    exercise = Exercise(
        name=data['name'],
        muscle_group=data['muscle_group'],
        description=data.get('description')
    )
    db.session.add(exercise)
    db.session.commit()
    
    return jsonify(exercise_schema.dump(exercise)), 201

# DELETE exercise
@exercises_bp.route('/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    
    return jsonify({'message': 'Exercise deleted successfully'}), 200