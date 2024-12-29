# Voxion

Voxion is a powerful speech recognition and annotation system that supports multilingual speech recognition and annotation management. It uses the OpenAI Whisper model for speech recognition and integrates with the Codatta platform for data annotation management.

## Features

- Multilingual speech recognition support (Chinese, English, Japanese, Korean, etc.)
- Real-time voice recording and recognition
- Multiple Whisper models available (from fast to high accuracy)
- Seamless integration with Codatta platform
- Offline model download and usage support
- User-friendly web interface

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/voxion.git
cd voxion
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the application:
```bash
python -m flask run --port=5002 --debug
```

5. Access the application:
```
http://localhost:5002
```

## Technology Stack

- Backend: Python Flask
- Speech Recognition: OpenAI Whisper
- Frontend: HTML5, JavaScript
- Audio Processing: MediaRecorder API

## Codatta Integration APIs

### 1. Redirect from Codatta to ASR
Handles user redirection from Codatta platform to ASR system for annotation.

**Endpoint**
```
GET /asr/task
```

**Request Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Codatta user authentication token |
| task_id | string | Yes | Codatta task ID |

**Response Status Codes**
- 200: Success, redirects to ASR annotation page
- 401: Invalid token
- 404: Task not found
- 400: Missing required parameters

**Example**
```
http://localhost:5002/asr/task?token=user_token_123&task_id=task_456
```

### 2. Submit Annotation to Codatta
Submits annotation data back to Codatta platform.

**Endpoint**
```
POST https://api.codatta.com/v1/annotations
```

**Request Headers**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**
```json
{
    "task_id": "string",      // Codatta task ID
    "audio_data": "string",   // Base64 encoded audio data
    "transcription": "string", // Transcribed text
    "language": "string",     // Audio language
    "model": "string",        // Model used
    "timestamp": "string"     // ISO format timestamp
}
```

**Response Status Codes**
- 200: Successfully submitted
- 401: Invalid token
- 404: Task not found
- 400: Invalid request data format

**Response Example**
```json
{
    "status": "success",
    "annotation_id": "annotation_789"
}
```

### Development Mode
For testing Codatta integration in development environment:

1. Enable mock mode:
```bash
export MOCK_CODATTA_API=true
```

2. Use test token (prefixed with "mock_"):
```
http://localhost:5002/asr/task?token=mock_user_123&task_id=task_456
```

3. Mock responses are configured in `config.py`:
```python
MOCK_RESPONSES = {
    'submit_annotation': {
        'status': 'success',
        'annotation_id': 'mock_annotation_123'
    }
}
```

### Production Configuration
When deploying to production:

1. Set correct API URL:
```bash
export CODATTA_API_BASE_URL=https://api.codatta.com/v1
```

2. Disable mock mode:
```bash
export MOCK_CODATTA_API=false
```

3. Set secure session key:
```bash
export FLASK_SECRET_KEY=your_secure_key
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
