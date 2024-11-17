from openai import AzureOpenAI
import os
import logging
from dotenv import load_dotenv
import json
import uuid
import time
import requests

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def generate_scene_image_1(text):
    try:
        time.sleep(3)
        client = AzureOpenAI(
            azure_endpoint="https://slideoo-editor-dalle.openai.azure.com/",
            api_key=os.getenv("DALLE_OPENAI_API_KEY"),
            api_version="2024-02-01",
        )

        logging.info("Generating Images..I")
        response = client.images.generate(
            prompt=text,
            model="Dalle3",
            size='1024x1024',
            n=1,
        )
        json_response = json.loads(response.model_dump_json())
        image_urls = [json_response["data"][0]["url"]]
        return image_urls
    except Exception as e:
        logging.error(e)
        return generate_images_bing_1(text)


def generate_scene_image_2(text):
    try:
        time.sleep(3)
        client = AzureOpenAI(
            azure_endpoint="https://slideoo.openai.azure.com/",
            api_key=os.getenv("DALLE_OPENAI_API_KEY_1"),
            api_version="2024-02-01",
        )

        logging.info("Generating Images..II")
        response = client.images.generate(
            prompt=text,
            model="Dalle3",
            size='1024x1024',
            n=1,
        )
        json_response = json.loads(response.model_dump_json())
        image_urls = [json_response["data"][0]["url"]]
        return image_urls
    except Exception as e:
        logging.error(e)
        return generate_images_bing_2(text)


def generate_images_bing_1(text):
    logging.info("Generating BING...")
    subscription_key = os.getenv("BING_SUBSCRIPTION_KEY")
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_term = "AI concept futuristic surreal abstract " + text
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "license": "ShareCommercially", 'imageType': 'Photo', 'size': 'All',
              "minheight": "1024", "minwidth": "1024", "count": 2}

    response = requests.get(search_url, headers=headers, params=params)
    search_results = response.json()

    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:1]]
    return thumbnail_urls


def generate_images_bing_2(text):
    logging.info("Generating BING...")
    subscription_key = os.getenv("BING_SUBSCRIPTION_KEY")
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_term = "AI fantasy surreal " + text + " art illustration"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "license": "ShareCommercially", 'imageType': 'Photo', 'size': 'All',
              "minheight": "1024", "minwidth": "1024", "count": 2}

    response = requests.get(search_url, headers=headers, params=params)
    search_results = response.json()

    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:1]]
    return thumbnail_urls


def save_images_locally(image_urls, directory, prefix):
    """
    Downloads images from URLs and saves them in the specified directory with a given prefix.
    """
    logging.info("Saving locally...")
    os.makedirs(directory, exist_ok=True)

    for idx, url in enumerate(image_urls, start=1):
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(directory, f"{prefix}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download image from {url}")


def create_images_for_prompts(prompts_dict):
    """
    Generates and saves images for each prompt in the dictionary, returning local paths for saved images.
    """

    unique_dir = str(uuid.uuid4())
    os.makedirs(unique_dir, exist_ok=True)

    saved_image_paths = {}

    for i, (key, prompt) in enumerate(prompts_dict.items(), start=1):
        if prompt:
            logging.info(f"{prompt}--{i}")
            try:
                image_url_1 = generate_scene_image_1(prompt)
                image_url_2 = generate_scene_image_2(prompt)
                prefix_1 = f"{key}_1"
                prefix_2 = f"{key}_2"

                save_images_locally(image_url_1, unique_dir, prefix_1)
                save_images_locally(image_url_2, unique_dir, prefix_2)

                saved_image_paths[key] = [os.path.join(unique_dir, f"{prefix_1}.png"), os.path.join(unique_dir, f"{prefix_2}.png")]
            except Exception as e:
                logging.info(f"Error generating images for {key}: {e}")
                saved_image_paths[key] = None
        else:
            saved_image_paths[key] = None
    logging.info("Image Generation Successful")
    return saved_image_paths

