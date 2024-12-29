"""Codatta integration service"""

import json
import requests
from datetime import datetime
from typing import Dict, Optional

from config import (
    CODATTA_API_BASE_URL,
    CODATTA_API_TIMEOUT,
    MOCK_CODATTA_API,
    MOCK_RESPONSES
)

class CodattaService:
    def __init__(self):
        self.base_url = CODATTA_API_BASE_URL
        self.timeout = CODATTA_API_TIMEOUT
        self.mock_mode = MOCK_CODATTA_API

    def validate_token(self, token: str) -> bool:
        """Validate Codatta user token"""
        if self.mock_mode:
            return token.startswith('mock_')
        
        try:
            response = requests.get(
                f"{self.base_url}/validate-token",
                headers={'Authorization': f'Bearer {token}'},
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def submit_annotation(self, token: str, data: Dict) -> Optional[Dict]:
        """Submit annotation data to Codatta"""
        if self.mock_mode:
            return MOCK_RESPONSES['submit_annotation']

        try:
            response = requests.post(
                f"{self.base_url}/annotations",
                headers={'Authorization': f'Bearer {token}'},
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error submitting to Codatta: {str(e)}")
            return None

    def format_annotation_data(self, task_id: str, audio_data: str, 
                             transcription: str, language: str, model: str) -> Dict:
        """Format annotation data for Codatta API"""
        return {
            "task_id": task_id,
            "audio_data": audio_data,
            "transcription": transcription,
            "language": language,
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        }
