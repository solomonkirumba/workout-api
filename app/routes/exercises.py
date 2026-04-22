from flask import Blueprint, request, jsonify
from app import db
from app.models.exercise import Exercise
from app.schemas.schemas import ExerciseSchema

exercises_bp = Blueprint('exercises', __name__)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

# GET all exercises (with pagination)
@exercises_bp.route('/', methods=['GET'])
def get_exercises():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 50)
    
    paginated = Exercise.query.order_by(Exercise.id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'exercises': exercises_schema.dump(paginated.items),
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'pages': paginated.pages,
        'has_next': paginated.has_next,
        'has_prev': paginated.has_prev
    }), 200

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
    
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
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