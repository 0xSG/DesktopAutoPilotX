import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from services.ollama_service import OllamaService
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///automation.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    db.init_app(app)

    # Ensure static folder exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Create static subdirectories if they don't exist
    for folder in ['screenshots', 'css', 'js', 'img']:
        folder_path = os.path.join('static', folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    class Task(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        description = db.Column(db.String(500), nullable=False)
        analysis = db.Column(db.Text)
        execution_plan = db.Column(db.Text)
        status = db.Column(db.String(50), default='pending')

        def __init__(self, description=None, analysis=None, execution_plan=None, status='pending'):
            self.description = description
            self.analysis = analysis
            self.execution_plan = execution_plan
            self.status = status

    ollama_service = OllamaService()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/analyze', methods=['POST'])
    def analyze_task():
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        data = request.get_json()
        task = data.get('task') if data else None
        if not task:
            return jsonify({'error': 'No task provided'}), 400
        
        # Get analysis from Ollama
        analysis = ollama_service.generate_analysis(task)
        
        # Create a new task record
        new_task = Task(
            description=task,
            analysis=analysis,
            status='analyzed'
        )
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({'analysis': new_task.analysis})

    @app.route('/execute', methods=['POST'])
    def execute_task():
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        data = request.get_json()
        task = data.get('task') if data else None
        if not task:
            return jsonify({'error': 'No task provided'}), 400
        
        # Find or create task
        db_task = Task.query.filter_by(description=task).first()
        if not db_task:
            db_task = Task(description=task)
            analysis = ollama_service.generate_analysis(task)
            db_task.analysis = analysis
        
        # Generate execution plan
        execution_plan = ollama_service.generate_execution_plan(task, db_task.analysis)
        db_task.execution_plan = execution_plan
        db_task.status = 'planned'
        db.session.add(db_task)
        db.session.commit()
        
        return jsonify({'plan': db_task.execution_plan})

    with app.app_context():
        db.create_all()

    return app
