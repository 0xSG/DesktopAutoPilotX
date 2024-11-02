from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db, ollama_service, screenshot_service, automation_service
from models import Task, AutomationLog
from datetime import datetime
import json

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/task/create', methods=['POST'])
def create_task():
    description = request.form.get('description')
    if not description:
        flash('Task description is required', 'danger')
        return jsonify({'error': 'Description required'}), 400
    
    # Create new task
    task = Task()
    task.description = description
    task.status = 'pending'
    db.session.add(task)
    db.session.commit()
    
    try:
        # Get AI reasoning if available
        if ollama_service:
            reasoning_result = ollama_service.get_reasoning(description)
            if reasoning_result['success']:
                task.ai_reasoning = json.dumps({
                    'reasoning': reasoning_result['reasoning'],
                    'steps': reasoning_result['steps']
                })
            else:
                app.logger.error(f"AI reasoning failed: {reasoning_result['error']}")
        
        # Take initial screenshot if available
        if screenshot_service:
            screenshot_path = screenshot_service.take_screenshot()
            task.screenshot_path = screenshot_path
            
            # Analyze screenshot with LLaVA if available
            if ollama_service and screenshot_path:
                analysis_result = ollama_service.analyze_image(screenshot_path)
                if analysis_result['success']:
                    # Create automation actions based on UI analysis
                    detected_elements = analysis_result['elements']
                    
                    # Execute actions based on detected elements
                    if automation_service and detected_elements:
                        for element in detected_elements:
                            action = {
                                "type": "analyze",
                                "element": element
                            }
                            
                            success = automation_service.execute_action(action)
                            log = AutomationLog()
                            log.task_id = task.id
                            log.action = f"Analyzed UI element: {json.dumps(element)}"
                            log.success = success
                            db.session.add(log)
                else:
                    app.logger.error(f"Image analysis failed: {analysis_result['error']}")
            
        task.status = 'completed'
        task.completed_at = datetime.utcnow()
        
    except Exception as e:
        app.logger.error(f"Task execution failed: {str(e)}")
        task.status = 'failed'
        log = AutomationLog()
        log.task_id = task.id
        log.action = f"Task failed: {str(e)}"
        log.success = False
        log.error_message = str(e)
        db.session.add(log)
    
    db.session.commit()
    return jsonify({'task_id': task.id})

@app.route('/task/<int:task_id>/status')
def task_status(task_id):
    task = Task.query.get_or_404(task_id)
    latest_log = AutomationLog.query.filter_by(task_id=task_id).order_by(AutomationLog.timestamp.desc()).first()
    
    # Parse AI reasoning if available
    ai_analysis = None
    if task.ai_reasoning:
        try:
            ai_analysis = json.loads(task.ai_reasoning)
        except:
            ai_analysis = {"reasoning": task.ai_reasoning}
    
    return jsonify({
        'status': task.status,
        'message': latest_log.action if latest_log else 'No updates',
        'screenshot': task.screenshot_path if task.screenshot_path else None,
        'ai_analysis': ai_analysis
    })
