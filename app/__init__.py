# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints
    from app.routes.workouts import workouts_bp
    from app.routes.exercises import exercises_bp
    
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(exercises_bp, url_prefix='/exercises')
    
    return app