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


def reddit_story_generator(story, language):
    logging.info("Article Based Story....")
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
    job = "Transform a Reddit story into a cohesive six-scene narrative while maintaining its original tone, theme, and structure."
    prompt = f"""
    Take the following Reddit story '{story}' provided by the user and convert it into a structured narrative divided into six scenes in {language} language. 

    Requirements:
    - Start with a compelling hook that aligns with the story's theme and immediately grabs attention.
    - Maintain the key elements, tone, and theme of the original Reddit story without altering its essence.
    - Divide the story into six interconnected scenes, each containing 20-22 words, ensuring smooth transitions between them.
    - Capture the main events, twists, or emotions from the original story in each scene, maintaining the same climax and conclusion.
    - Ensure that the ending reflects the resolution or conclusion provided in the Reddit story.
    - Use concise and engaging language, avoiding unnecessary additions or deviations from the original content.

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


# reddit_story = """
# Once Upon a Heartbreak
#
# I used to imagine myself as the main character, the shy girl who catches the eye of the tall, dark, and handsome guy. But yeah, maybe my imagination was a bit much.
#
# Then, he happened. It's a blur now, like a cheesy Netflix rom-com. He wasn't Prince Charming, but his smile could melt glaciers. It was like the universe said, "Here's your guy," and who was I to argue? We clicked instantly. Late-night chats, sharing secrets, the kind of intimacy that makes your soul feel seen. He had this energy that pulled me out of my shell. I gave him a safe space to be himself.
#
# Months flew by, and suddenly, we were building castles in the clouds, whispering about a future that felt so real.  No more fictional crushes. Just us, raw and real. Two years. Two incredible and perfect years of a love that felt invincible. We were the "it" couple. But then, life happened.
#
# College hit us hard. The pressure, the assignments, the doubts – it all chipped away at us. Fights, unsaid words, and our love story ended with a sad look as we realized we were better off apart. The pain was awful. Every love song felt like a punch in the gut. But as the shock faded, I knew I wouldn't trade those two years for anything. The ache in my chest reminded me that I'd experienced something real, something precious. Losing him taught me love isn't a fairytale. It's messy and unpredictable, and sometimes it hurts. But it's also the most incredible feeling, a leap of faith worth taking.
#
# My love story with him wasn't perfect, but it burned bright. It reminded me that real love exists, not just in books or movies. Love might break your heart, but it also makes you see how beautiful and complicated life can be. I'm wiser now, more cautious, but still hopeful. Because even a moment of fireworks is better than a lifetime of darkness.
# """
#
# lang = "English"
#
# scenes = reddit_story_generator(reddit_story, lang)
# print(json.dumps(scenes, indent=4))