import requests
from dotenv import load_dotenv
import os
import logging
import uuid

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_adam_legacy_voice(text):
    try:
        logging.info("Voice Generation..I")
        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.9
            }
        }
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": os.getenv('ELEVEN_LABS_API_KEY_1')
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error: {response.status_code}, {response.json()}")
    except Exception as ev1:
        logging.info("Voice Generation..II")
        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.9
            }
        }
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": os.getenv('ELEVEN_LABS_API_KEY_2')
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error: {response.status_code}, {response.json()}")


def create_audio_files(text_dict):
    """
    Generates audio files for six text inputs and saves them in a unique directory.
    """
    unique_dir = str(uuid.uuid4())
    os.makedirs(unique_dir, exist_ok=True)
    saved_audio_paths = {}
    for i, (scene, text) in enumerate(text_dict.items(), start=1):
        audio_data = generate_adam_legacy_voice(text)

        file_path = os.path.join(unique_dir, f"sound_{i}.mp3")
        with open(file_path, "wb") as f:
            f.write(audio_data)
        saved_audio_paths[scene] = file_path

    return saved_audio_paths

