"""Configuration module"""

import os
import secrets

# Flask configuration
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# Language configurations
LANGUAGES = {
    # East Asian languages
    'zh': {'name': 'Chinese (Mandarin)', 'description': 'Chinese Mandarin'},
    'zh-tw': {'name': 'Chinese (Taiwan)', 'description': 'Traditional Chinese (Taiwan)'},
    'zh-hk': {'name': 'Chinese (Hong Kong)', 'description': 'Traditional Chinese (Hong Kong)'},
    'zh-cn-sichuan': {'name': 'Chinese (Sichuan Dialect)', 'description': 'Sichuan Dialect'},
    'zh-cn-cantonese': {'name': 'Chinese (Cantonese)', 'description': 'Cantonese'},
    'ja': {'name': 'Japanese', 'description': 'Japanese'},
    'ko': {'name': 'Korean', 'description': 'Korean'},

    # Southeast Asian languages
    'vi': {'name': 'Vietnamese', 'description': 'Vietnamese'},
    'th': {'name': 'Thai', 'description': 'Thai'},
    'id': {'name': 'Indonesian', 'description': 'Indonesian'},
    'ms': {'name': 'Malay', 'description': 'Malay'},

    # South Asian languages
    'hi': {'name': 'Hindi', 'description': 'Hindi'},
    'ta': {'name': 'Tamil', 'description': 'Tamil'},
    'ur': {'name': 'Urdu', 'description': 'Urdu'},

    # European languages
    'en': {'name': 'English', 'description': 'English'},
    'fr': {'name': 'French', 'description': 'French'},
    'de': {'name': 'German', 'description': 'German'},
    'es': {'name': 'Spanish', 'description': 'Spanish'},
    'it': {'name': 'Italian', 'description': 'Italian'},
    'pt': {'name': 'Portuguese', 'description': 'Portuguese'},
    'ru': {'name': 'Russian', 'description': 'Russian'},

    # Middle Eastern languages
    'ar': {'name': 'Arabic', 'description': 'Arabic'},
    'fa': {'name': 'Persian', 'description': 'Persian'},
    'tr': {'name': 'Turkish', 'description': 'Turkish'},

    # African languages
    'sw': {'name': 'Swahili', 'description': 'Swahili'},
    'am': {'name': 'Amharic', 'description': 'Amharic'},
}

# Model configurations with descriptions
WHISPER_MODELS = {
    'tiny': {
        'name': 'Tiny',
        'description': 'Fastest, less accurate',
        'size_mb': 150
    },
    'base': {
        'name': 'Base',
        'description': 'Fast, balanced accuracy',
        'size_mb': 300
    },
    'small': {
        'name': 'Small',
        'description': 'Good accuracy, moderate speed',
        'size_mb': 1000
    },
    'medium': {
        'name': 'Medium',
        'description': 'High accuracy, slower',
        'size_mb': 2500
    },
    'large': {
        'name': 'Large',
        'description': 'Highest accuracy, slowest',
        'size_mb': 6000
    }
}

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
