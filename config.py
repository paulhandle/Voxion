"""Configuration module"""

import os
import secrets

# Flask configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# UI Language configurations (for Babel)
BABEL_DEFAULT_LOCALE = 'en'
BABEL_TRANSLATION_DIRECTORIES = 'translations'

SUPPORTED_UI_LANGUAGES = ['en', 'zh']
UI_LANGUAGE_NAMES = {
    'en': 'English',
    'zh': '中文'
}

# Speech Recognition Language configurations
SPEECH_LANGUAGES = {
    # East Asian languages
    'zh': {'name': 'Chinese (Mandarin)', 'description': '普通话'},
    'zh-hk': {'name': 'Chinese (Cantonese)', 'description': '广东话'},
    'ja': {'name': 'Japanese', 'description': '日本語'},
    'ko': {'name': 'Korean', 'description': '한국어'},

    # European languages
    'en': {'name': 'English', 'description': 'English'},
    'fr': {'name': 'French', 'description': 'Français'},
    'de': {'name': 'German', 'description': 'Deutsch'},
    'es': {'name': 'Spanish', 'description': 'Español'},
    'it': {'name': 'Italian', 'description': 'Italiano'},
    'pt': {'name': 'Portuguese', 'description': 'Português'},
    'ru': {'name': 'Russian', 'description': 'Русский'},

    # Southeast Asian languages
    'vi': {'name': 'Vietnamese', 'description': 'Tiếng Việt'},
    'th': {'name': 'Thai', 'description': 'ภาษาไทย'},
    'id': {'name': 'Indonesian', 'description': 'Bahasa Indonesia'},
    'ms': {'name': 'Malay', 'description': 'Bahasa Melayu'},

    # South Asian languages
    'hi': {'name': 'Hindi', 'description': 'हिन्दी'},
    'ta': {'name': 'Tamil', 'description': 'தமிழ்'},
    'ur': {'name': 'Urdu', 'description': 'اردو'}
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
