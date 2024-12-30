"""Configuration module"""

import os
import secrets

# Flask configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# Language configurations
BABEL_DEFAULT_LOCALE = 'en'
BABEL_TRANSLATION_DIRECTORIES = 'translations'

SUPPORTED_LANGUAGES = ['en', 'zh']
LANGUAGE_NAMES = {
    'en': 'English',
    'zh': '中文'
}

# Whisper model configurations
WHISPER_MODELS = {
    'tiny': {'name': 'Tiny', 'size': '75M'},
    'base': {'name': 'Base', 'size': '142M'},
    'small': {'name': 'Small', 'size': '466M'},
    'medium': {'name': 'Medium', 'size': '1.5G'},
    'large': {'name': 'Large', 'size': '2.9G'},
}

# File upload configurations
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Codatta API configuration
CODATTA_API_BASE_URL = os.getenv('CODATTA_API_BASE_URL', 'https://api.codatta.com/v1')
CODATTA_API_TIMEOUT = 30

# Mock mode for development
MOCK_CODATTA_API = os.getenv('MOCK_CODATTA_API', 'true').lower() == 'true'

# Mock responses
MOCK_RESPONSES = {
    'submit_annotation': {
        'status': 'success',
        'annotation_id': 'mock_annotation_123'
    }
}
