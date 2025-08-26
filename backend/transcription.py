import os
import requests

# Use this to call the transcription Flask service

def transcribe_audio_via_service(file_path):
    url = 'http://transcription_service:5001/transcribe'
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.json().get('transcription', '')
    else:
        raise Exception(f"Transcription service error: {response.status_code} {response.text}")
