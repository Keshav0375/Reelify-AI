import boto3
from openai import AzureOpenAI
import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bedrock = boto3.client(service_name="bedrock-runtime",
                           aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                           aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                           region_name="us-east-1")

client = AzureOpenAI(
  azure_endpoint=os.getenv('AZURE_ENDPOINT_4O'),
  api_key=os.getenv('AZURE_API_KEY_4O'),
  api_version=os.getenv('AZURE_VERSION_4O')
)

def story_generator(topic, theme, language):
    logging.info("Generating story....")
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    example_response = {
        "scene_1": "",
        "scene_2": "",
        "scene_3": "",
        "scene_4": "",
        "scene_5": "",
        "scene_6": ""
    }
    accept = "application/json"
    contentType = "application/json"
    job = "You are a creative assistant generating a detailed, suspenseful, and engaging storyline divided into six interconnected scenes."
    prompt = f"""
    Create a compelling story based on the topic '{topic}' and theme '{theme}', written in '{language}'.
    The story must:
    - Be divided into six scenes, each with 22-24 words.
    - Begin with an emotionally engaging hook tailored to the theme to captivate the audience immediately.
    - Maintain a suspenseful and interconnected narrative throughout, building curiosity and anticipation between scenes.
    - Use twists, cliffhangers, and vivid imagery to keep the audience engaged.
    - Conclude with a memorable and impactful ending that resonates with the theme and leaves a lasting impression.
    
    Additional Requirements:
    - Match the mood, tone, and style of the chosen theme in every scene.
    - Ensure smooth and logical transitions between scenes for a cohesive story arc.
    - Use simple, universally understandable language suitable for a diverse audience.
    - Align the narrative with the fast-paced, high-impact nature of short reels or social media videos.
    
    Strictly return the output in the format of a Python dictionary or JSON without any additional text or explanation.
    """


    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "messages": [
                        {
                            "role": "user",
                            "content": job
                        },
                        {
                            "role": "assistant",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": f"Example response:\n{json.dumps(example_response, indent=4)}"
                        }

                    ],
                }),
            accept=accept,
            contentType=contentType
        )
        result = json.loads(response.get('body').read())
        content = result['content'][0]['text']
        j_ = json.loads(content)

    except Exception as ellm:
        logging.info(f"Trying to get response from gpt 4o: {ellm}")
        response = client.chat.completions.create(
            model="slideoo-2-gpt-40",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": job
                },
                {
                    "role": "assistant",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"Example response:\n{json.dumps(example_response, indent=4)}"
                }
            ],
            temperature=0.9,
            n=1,
            max_tokens=4000)

        j_ = json.loads(response.choices[0].message.content)
    logging.info("Story Generation Successful")
    return j_


def image_prompt_generator(topic, theme, language, scenes):
    logging.info("Generating search terms....")
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    example_response = {
        "prompt_1": "",
        "prompt_2": "",
        "prompt_3": "",
        "prompt_4": "",
        "prompt_5": "",
        "prompt_6": ""
    }
    accept = "application/json"
    contentType = "application/json"
    job = "You are a creative assistant generating short, visually descriptive prompts for AI image generation. For each scene in a short reel, you will create a 2-5 word prompt that captures the scene’s core visuals and mood. Prompts should be simple, directly related to the scene content, and aligned with the reel’s theme and style."
    prompt = f"""
    Based on the following scenes, generate a in detailed 7-9 word image prompt for each one. Each prompt should be visually descriptive, capturing the main idea and atmosphere of each scene for AI image generation. The reel is themed around '{theme}' and is based on the topic '{topic}', in the English language.
    
    Scenes:
    {scenes}
    
     For each scene, your task is to:
        - Create a simple, clear visual prompt that is easy to understand and directly reflects the scene’s content.
        - Match the prompt with the theme '{theme}', incorporating its mood, tone, and style.
        - Use gentle, positive language, focusing on key visuals or actions without complex, abstract, or sensitive words (e.g., avoid terms related to violence, harm, or intense emotions).
        - Rephrase any potentially sensitive terms to be softer or more neutral. Prioritize words that evoke positive, safe, and inviting visuals.
        - Ensure each prompt connects visually and thematically to its corresponding scene, forming a cohesive set.
        - Prompts should not violate content policy or include any content that could be flagged. 

    Strictly return the output in the format of a Python dictionary or JSON without any additional text or explanation.
    """

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "messages": [
                        {
                            "role": "user",
                            "content": job
                        },
                        {
                            "role": "assistant",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": f"Example response:\n{json.dumps(example_response, indent=4)}"
                        }

                    ],
                }),
            accept=accept,
            contentType=contentType
        )
        result = json.loads(response.get('body').read())
        content = result['content'][0]['text']
        j_ = json.loads(content)

    except Exception as ellm:
        logging.info(f"Trying to get response from claude 3: {ellm}")
        response = client.chat.completions.create(
            model="slideoo-2-gpt-40",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": job
                },
                {
                    "role": "assistant",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"Example response:\n{json.dumps(example_response, indent=4)}"
                }
            ],
            temperature=0.9,
            n=1,
            max_tokens=4000)

        j_ = json.loads(response.choices[0].message.content)
    logging.info("Search Prompts Created")
    return j_

