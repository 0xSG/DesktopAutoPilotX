from flask import render_template, request, jsonify, flash
from app import app, ollama_service, screenshot_service, automation_service
from models import Task, AutomationLog, db
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models/list')
def list_models():
    try:
        if ollama_service and ollama_service.registry:
            models = ollama_service.registry.list_models()
            
            # Categorize models by capability
            vision_models = []
            reasoning_models = []
            
            for model_id, config in models.items():
                model_info = {
                    'id': model_id,
                    'name': config.get('model', model_id),
                    'description': config.get('description', '')
                }
                
                if 'vision' in config.get('capabilities', []):
                    vision_models.append(model_info)
                if 'text' in config.get('capabilities', []):
                    reasoning_models.append(model_info)
            
            return jsonify({
                'vision': vision_models,
                'reasoning': reasoning_models
            })
        else:
            return jsonify({'error': 'Model registry not available'}), 503
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/settings/update', methods=['POST'])
def update_settings():
    try:
        settings = request.get_json()
        if not settings:
            return jsonify({"error": "No settings data provided"}), 400
            
        if not isinstance(settings, dict) or 'models' not in settings:
            return jsonify({"error": "Invalid settings format"}), 400
            
        models = settings.get('models', {})
        if not isinstance(models, dict):
            return jsonify({"error": "Invalid models format"}), 400
            
        # Update model selections in registry
        if ollama_service and ollama_service.registry:
            # Validate model selections
            available_models = ollama_service.registry.list_models()
            
            vision_model = models.get('vision')
            reasoning_model = models.get('reasoning')
            
            if vision_model and vision_model not in available_models:
                return jsonify({"error": f"Invalid vision model: {vision_model}"}), 400
            if reasoning_model and reasoning_model not in available_models:
                return jsonify({"error": f"Invalid reasoning model: {reasoning_model}"}), 400
            
            # Update selected models
            ollama_service.registry.selected_models = {
                'vision': vision_model,
                'reasoning': reasoning_model
            }
        
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Settings update failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'database': db is not None,
        'ollama_service': ollama_service is not None,
        'screenshot_service': screenshot_service is not None,
        'automation_service': automation_service is not None
    })

@app.route('/history')
def history():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('history.html', tasks=tasks)
