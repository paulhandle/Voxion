"""Transcription service module"""

import os
import whisper
import ssl
import urllib.request
import time
from config import WHISPER_MODELS
import torch
from typing import Dict, List

# Cache loaded models
_loaded_models = {}

def download_with_retry(url, max_retries=3, retry_delay=1):
    """
    Download function with retry mechanism
    
    Args:
        url: Download URL
        max_retries: Maximum number of retries
        retry_delay: Retry delay in seconds
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(url, context=ctx) as response:
                return response.read()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(retry_delay)
            continue

def get_model(model_name='base'):
    """
    Get or load specified Whisper model
    
    Args:
        model_name (str): Model name, must be one of WHISPER_MODELS
        
    Returns:
        Model instance
    """
    if model_name not in WHISPER_MODELS:
        raise ValueError(f"Unsupported model: {model_name}")
    
    if model_name not in _loaded_models:
        try:
            # Set SSL context
            ssl._create_default_https_context = ssl._create_unverified_context
            _loaded_models[model_name] = whisper.load_model(model_name)
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}. Please check network connection and retry.")
    
    return _loaded_models[model_name]

def get_downloaded_models() -> List[str]:
    """Get list of already downloaded Whisper models
    
    Returns:
        List[str]: List of model names that are already downloaded
    """
    # Check ~/.cache/whisper directory for downloaded models
    cache_dir = os.path.expanduser("~/.cache/whisper")
    if not os.path.exists(cache_dir):
        return []
        
    downloaded = []
    for model in ['tiny', 'base', 'small', 'medium', 'large']:
        model_path = os.path.join(cache_dir, f'{model}.pt')
        if os.path.exists(model_path):
            downloaded.append(model)
            
    return downloaded

def transcribe_audio(audio_path: str, language: str, model_name: str = 'base') -> Dict:
    """
    Transcribe audio file using Whisper model
    
    Args:
        audio_path (str): Path to audio file
        language (str): Language code (e.g., 'en', 'zh')
        model_name (str): Whisper model name (default: 'base')
        
    Returns:
        Dict: Transcription result containing text and segments
        
    Raises:
        Exception: If transcription fails
    """
    try:
        # Get specified model
        model = get_model(model_name)
        
        # Configure transcription options
        transcribe_options = {
            'task': 'transcribe',
            'language': language if language != 'auto' else None
        }
        
        # Perform transcription
        result = model.transcribe(audio_path, **transcribe_options)
        
        # Extract result, including time axis information
        segments = []
        for segment in result["segments"]:
            segments.append({
                'id': segment['id'],
                'text': segment['text'].strip(),
                'start': segment['start'],
                'end': segment['end'],
                'words': segment.get('words', [])  # Some models may not provide word-level time axis
            })
        
        # Delete temporary file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return {
            'text': result["text"],
            'detected_language': result.get("language", "unknown"),
            'segments': segments
        }
        
    except Exception as e:
        # Ensure cleanup of temporary file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        # Provide more friendly error message
        error_message = str(e)
        if "SSL" in error_message:
            error_message = "Network connection is unstable, please retry. If the problem persists, please check network settings."
        elif "CUDA" in error_message:
            error_message = "GPU memory is insufficient, please try using a smaller model or using CPU mode."
        elif "memory" in error_message.lower():
            error_message = "System memory is insufficient, please try using a smaller model."
            
        raise Exception(error_message)
    finally:
        # Clean up CUDA memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
