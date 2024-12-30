from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, g
from flask_babel import get_locale
import os
import uuid
import json
from config import SUPPORTED_LANGUAGES, WHISPER_MODELS, LANGUAGE_NAMES
from services.transcription import transcribe_audio, get_downloaded_models
from services.codatta import CodattaService

main_bp = Blueprint('main', __name__)

# Initialize Codatta service
codatta_service = CodattaService()

@main_bp.before_request
def before_request():
    """Set language code for templates"""
    g.lang_code = str(get_locale())

@main_bp.route('/set_language/<lang>')
def set_language(lang):
    """Set the user's preferred language"""
    session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/')
def index():
    """Render main page"""
    downloaded_models = get_downloaded_models()
    return render_template('index.html', 
                         languages=LANGUAGE_NAMES,
                         models=WHISPER_MODELS,
                         downloaded_models=downloaded_models)

@main_bp.route('/transcribe', methods=['POST'])
def handle_transcribe():
    """Handle audio transcription request"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    language = request.form.get('language', 'auto')
    model = request.form.get('model', 'base')
    
    # Ensure upload directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Generate unique filename
    filename = str(uuid.uuid4()) + '.wav'
    filepath = os.path.join('uploads', filename)
    
    # Save audio file
    audio_file.save(filepath)
    
    try:
        # Use transcription service
        result = transcribe_audio(filepath, language, model)
        return jsonify(result)
    except Exception as e:
        # If error, ensure delete temporary file
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

@main_bp.route('/save-annotation', methods=['POST'])
def save_annotation():
    """Save annotation information"""
    try:
        data = request.json
        if not data or 'segments' not in data:
            return jsonify({'error': 'Invalid data format'}), 400
        
        # Ensure annotation directory exists
        os.makedirs('annotations', exist_ok=True)
        
        # Generate unique annotation filename
        annotation_id = str(uuid.uuid4())
        filepath = os.path.join('annotations', f'{annotation_id}.json')
        
        # Save annotation
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'annotation_id': annotation_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    return jsonify(SUPPORTED_LANGUAGES)

@main_bp.route('/models', methods=['GET'])
def get_models():
    """Get list of supported models"""
    return jsonify(WHISPER_MODELS)

@main_bp.route('/asr/task')
def asr_task():
    """Handle Codatta redirect with token"""
    token = request.args.get('token')
    task_id = request.args.get('task_id')
    
    if not token or not task_id:
        return jsonify({'error': 'Missing required parameters'}), 400
        
    if not codatta_service.validate_token(token):
        return jsonify({'error': 'Invalid token'}), 401
        
    # Store token and task_id in session
    session['codatta_token'] = token
    session['codatta_task_id'] = task_id
    
    return redirect(url_for('index'))

@main_bp.route('/api/submit_annotation', methods=['POST'])
def submit_annotation():
    """Submit annotation to Codatta"""
    token = session.get('codatta_token')
    task_id = session.get('codatta_task_id')
    
    if not token or not task_id:
        return jsonify({'error': 'No active Codatta session'}), 401
        
    data = request.json
    if not data or 'audio_data' not in data or 'transcription' not in data:
        return jsonify({'error': 'Missing required data'}), 400
        
    annotation_data = codatta_service.format_annotation_data(
        task_id=task_id,
        audio_data=data['audio_data'],
        transcription=data['transcription'],
        language=data['language'],
        model=data['model']
    )
    
    result = codatta_service.submit_annotation(token, annotation_data)
    if not result:
        return jsonify({'error': 'Failed to submit annotation'}), 500
        
    return jsonify({})
