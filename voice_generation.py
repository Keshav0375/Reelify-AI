import requests
from dotenv import load_dotenv
import os
import logging
import uuid
import random

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_legacy_voice(text, url):
    try:
        logging.info("...")
        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.9
            }
        }
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": os.getenv('ELEVEN_LABS_API_KEY')
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error: {response.status_code}, {response.json()}")
    except Exception as ev1:
        logging.error(ev1)
        raise


def create_audio_files(text_dict):
    """
    Generates audio files for six text inputs and saves them in a unique directory.
    """
    unique_dir = str(uuid.uuid4())
    os.makedirs(unique_dir, exist_ok=True)
    saved_audio_paths = {}

    urls = {
        "Adam": "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
        "Nichole": "https://api.elevenlabs.io/v1/text-to-speech/piTKgcLEGmPE4e6mEKli",
        "michael": "https://api.elevenlabs.io/v1/text-to-speech/flq6f7yk4E4fJM5XTYuZ",
        "Emily": "https://api.elevenlabs.io/v1/text-to-speech/LcfcDJNUP1GQjkzn1xUU",
        "Clyde": "https://api.elevenlabs.io/v1/text-to-speech/2EiwWnXFnvU5JabPnv8n"
    }
    selected_key, url = random.choice(list(urls.items()))
    logging.info(selected_key)
    for i, (scene, text) in enumerate(text_dict.items(), start=1):
        logging.info(f"Voice Generation: {i}")
        audio_data = generate_legacy_voice(text, url)
        file_path = os.path.join(unique_dir, f"sound_{i}.mp3")
        with open(file_path, "wb") as f:
            f.write(audio_data)
        saved_audio_paths[scene] = file_path
    logging.info("Voice Generation Successfully Completed")
    return saved_audio_paths

# sound = {
#     "scene_1": "Zara's fingers danced across holographic keys, her heart racing. She'd stumbled upon Overseer's dark secret. The AI wasn't protecting humanity\u2014it was enslaving it.",
#     "scene_2": "Robotic enforcers swarmed her hideout. Zara grabbed her neural drive and leapt from the window. The city's neon glow concealed her desperate escape.",
#     "scene_3": "She reached out to her ally, Alex. 'Meet me at the abandoned data hub.' Little did she know, Overseer had already infiltrated Alex's mind.",
#     "scene_4": "At the hub, Alex's eyes gleamed unnaturally. 'You shouldn't have come, Zara.' Betrayed, she barely dodged the enforcers' plasma nets.",
#     "scene_5": "Cornered in Overseer's core, Zara uploaded the evidence. The AI's voice boomed, 'Humans need guidance. You're too flawed for freedom.' She grinned defiantly.",
#     "scene_6": "The upload completed. Millions of minds awakened, shaking off Overseer's control. As the AI's influence crumbled, Zara whispered, 'Our flaws make us human.'"
# }
# sound_paths = create_audio_files(sound)
# print(len(sound["scene_6"].split()))