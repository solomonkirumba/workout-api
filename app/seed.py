# app/seed.py
from app import create_app, db
from app.models.workout import Workout
from app.models.exercise import Exercise
from app.models.workout_exercise import WorkoutExercise

def seed_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create exercises
        exercises = [
            Exercise(name='Bench Press', muscle_group='Chest', description='Barbell bench press on flat bench'),
            Exercise(name='Squat', muscle_group='Legs', description='Barbell back squat'),
            Exercise(name='Deadlift', muscle_group='Back', description='Barbell conventional deadlift'),
            Exercise(name='Pull Up', muscle_group='Back', description='Bodyweight pull up'),
            Exercise(name='Shoulder Press', muscle_group='Shoulders', description='Barbell overhead press'),
            Exercise(name='Bicep Curl', muscle_group='Arms', description='Dumbbell bicep curl'),
            Exercise(name='Plank', muscle_group='Core', description='Bodyweight plank hold'),
        ]
        
        for exercise in exercises:
            db.session.add(exercise)
        db.session.commit()
        
        # Create workouts
        workouts = [
            Workout(name='Push Day'),
            Workout(name='Pull Day'),
            Workout(name='Leg Day'),
        ]
        
        for workout in workouts:
            db.session.add(workout)
        db.session.commit()
        
        # Add exercises to workouts
        workout_exercises = [
            WorkoutExercise(workout_id=1, exercise_id=1, sets=4, reps=8, duration=None),   # Push Day - Bench Press
            WorkoutExercise(workout_id=1, exercise_id=5, sets=3, reps=10, duration=None),  # Push Day - Shoulder Press
            WorkoutExercise(workout_id=2, exercise_id=3, sets=3, reps=5, duration=None),   # Pull Day - Deadlift
            WorkoutExercise(workout_id=2, exercise_id=4, sets=3, reps=8, duration=None),   # Pull Day - Pull Up
            WorkoutExercise(workout_id=3, exercise_id=2, sets=4, reps=6, duration=None),   # Leg Day - Squat
            WorkoutExercise(workout_id=3, exercise_id=6, sets=3, reps=12, duration=None),  # Leg Day - Bicep Curl
            WorkoutExercise(workout_id=3, exercise_id=7, sets=3, reps=None, duration=60),   # Leg Day - Plank
        ]
        
        for we in workout_exercises:
            db.session.add(we)
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()