import os
import shutil
import streamlit as st
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
from background_image import set_background
from prompts import story_generator, image_prompt_generator
from voice_generation import create_audio_files
from image_generation import create_images_for_prompts
from video_generator import create_video_without_captions
from caption_generation import add_fancy_captions
from reddit_story_generation import reddit_story_generator
import random
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(layout="wide", page_title="Reelify AI: Faceless Reels Creator")

if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = 'Home'

if 'temporary_files' not in st.session_state:
    st.session_state.temporary_files = []

with st.sidebar:
    selected_tab = option_menu("Menu",
                            ["Home", "Enter Your Topic", "Story Preview", "Preview Images", "Preview Sounds", "Get Your Video"],
                                icons=['house-heart-fill', 'file-earmark-richtext', 'pen', 'images', 'soundwave', 'camera-reels'],
                                menu_icon="cast", default_index=0,)



def track_temp_dir(dir_path):
    if dir_path not in st.session_state.temporary_files:
        st.session_state.temporary_files.append(dir_path)


def cleanup_temp_files():
    """Remove all temporary directories and clear the tracking list."""
    for dir_path in st.session_state.get("temporary_files", []):
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
        except Exception as e:
            logging.error(f"Error removing {dir_path}: {e}")
    st.session_state.temporary_files = []


if 'restart_triggered' not in st.session_state:
    st.session_state.restart_triggered = False

if selected_tab != st.session_state.selected_tab:
    st.session_state.selected_tab = selected_tab
    if st.session_state.selected_tab == 'Home':
        cleanup_temp_files()
        st.session_state.restart_triggered = False
        st.session_state.clear()
        st.rerun()

if 'last_active' not in st.session_state:
    st.session_state.last_active = datetime.now()

def check_inactivity_and_cleanup():
    """Automatically clean up if session is inactive for 5 minutes."""
    if datetime.now() - st.session_state.last_active > timedelta(minutes=5):
        cleanup_temp_files()
        st.session_state.last_active = datetime.now()


if st.session_state['selected_tab'] == 'Home':
    set_background("./helper_images/homepage.webp")
    st.markdown("""
                        <h1 
                        style='font-family: Georgia, serif; text-align: center;'>
                        Reelify AI: Your Personal Faceless Reels Creator
                        </h1>
                    """,
                unsafe_allow_html=True)
    st.write(
        """
        Welcome to Reelify AI! Effortlessly create captivating faceless reels with a single prompt. 
        Choose from diverse themes, and watch your ideas transform into engaging short videos, 
        optimized for virality on platforms like Instagram and YouTube. Start creating now!
        """)
    st.markdown("""
            <style>
                .features-title {
                    font-size: 2em;
                    color: #4A90E2;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .features-list {
                    font-size: 1.2em;
                    line-height: 1.6;
                }
                .feature-item {
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px 0;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
            </style>
            <div class="features-title">🌟 Key Features 🌟</div>
            <div class="features-list">
                <div class="feature-item">📄 Enter your topic and theme you want to create story upon.</div>
                <div class="feature-item">🔍 Preview images and sound.</div>
                <div class="feature-item">✍️ Get you video within ~ 3 minutes.</div>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state['selected_tab'] == "Enter Your Topic":
    st.markdown("<h2 style='text-align: center;'>Step 1: Define Your Story</h2>", unsafe_allow_html=True)
    options = [
        "A fast-paced, suspenseful story with a twist ending",
        "A humorous take on dating and relationships in today’s world",
        "A quick, magical journey with mythical creatures and epic battles",
        "Inspiring personal growth stories, highlighting resilience or success",
        "A glimpse into a futuristic world with tech-driven conflicts",
        "A cute, touching story featuring a rescued animal or pet",
        "A detective story with clues, suspense, and a satisfying resolution",
        "A reenactment of a significant historical event in 60 seconds",
        "A chilling story with jump-scares or eerie atmosphere",
        "A mini-narrative that provides quick, actionable life advice",
        "Heartfelt stories that emphasize family values and love",
        "A quick look at someone following their dreams against all odds",
        "A mini culinary journey, showcasing unique dishes or street food",
        "A captivating journey through beautiful, unexplored places",
        "An intriguing setup that encourages viewers to solve a riddle",
        "A fun, exaggerated portrayal of popular figures or characters",
        "Quick, useful tips shown through a mini DIY project or life hack",
        "A lighthearted take on awkward or funny day-to-day scenarios",
        "A short story set in a beautiful travel destination, offering an escape",
        "A snippet from a well-known cultural legend or myth, retold creatively"
    ]
    language_options = [
        "English",
        "Hindi"
    ]
    caption_options = [
        "Single Word Caption",
        "Multi Word Caption"
    ]

    with st.form("topic_form"):
        st.session_state.main_topic = st.text_input("Enter your topic:")
        st.session_state.theme = st.selectbox("Choose a theme:", options)
        st.session_state.language1 = st.selectbox("Choose a language:", language_options)
        topic_form_submitted = st.form_submit_button("Generate Story")

    with st.form("personalized_form"):
        st.session_state.personalized_topic = st.text_area("Enter your Reddit story:")
        st.session_state.language2 = st.selectbox("Choose a language:", language_options, key="language_2")
        personalized_form_submitted = st.form_submit_button("Generate Story")

    if topic_form_submitted and personalized_form_submitted:
        st.warning("Please fill out only one form.")
    elif topic_form_submitted:
        with st.spinner("Generating story..."):
            st.session_state.story_scenes = story_generator(st.session_state.main_topic, st.session_state.theme, st.session_state.language1)
            st.session_state.topic = st.session_state.main_topic
            st.session_state.language = st.session_state.language1
        st.session_state.selected_tab = 'Story Preview'
    elif personalized_form_submitted:
        with st.spinner("Generating story..."):
            st.session_state.story_scenes = reddit_story_generator(st.session_state.personalized_topic, st.session_state.language2)
            st.session_state.topic = st.session_state.personalized_topic
            st.session_state.language = st.session_state.language2
        st.session_state.selected_tab = 'Story Preview'
    elif not (topic_form_submitted or personalized_form_submitted):
        st.info("Fill one of the forms and click 'Generate Story'.")

elif st.session_state['selected_tab'] == 'Story Preview':
    st.markdown("<h2 style='text-align: center;'>Step 2: Story Scenes Preview</h2>", unsafe_allow_html=True)
    if 'story_scenes' in st.session_state:
        for i, scene in enumerate(st.session_state.story_scenes.values(), start=1):
            st.markdown(f"<p style='font-size: 1.2em;'>Scene {i}: {scene}</p>", unsafe_allow_html=True)

        with st.spinner("Generating image prompts..."):
            st.session_state.image_prompts = image_prompt_generator(st.session_state.topic, st.session_state.theme, st.session_state.language, st.session_state.story_scenes)
        st.session_state.selected_tab = 'Preview Images'
    else:
        st.write("Please go back and enter a topic to generate the story scenes.")

elif st.session_state['selected_tab'] == 'Preview Images':
    st.markdown("<h2 style='text-align: center;'>Step 3: Image Previews</h2>", unsafe_allow_html=True)
    if 'image_prompts' in st.session_state:
        with st.spinner("Generating images..."):
            st.session_state.image_paths = create_images_for_prompts(st.session_state.image_prompts)

        for i, (prompt, images) in enumerate(st.session_state.image_paths.items(), start=1):
            st.write(f"Prompt {i}:")
            for image_path in images:
                st.image(image_path, use_column_width=True)
                track_temp_dir(os.path.dirname(image_path))
        st.session_state.selected_tab = 'Preview Sounds'
    else:
        st.write("Please go back and preview the story scenes first.")

elif st.session_state['selected_tab'] == 'Preview Sounds':
    st.markdown("<h2 style='text-align: center;'>Step 4: Sound Previews</h2>", unsafe_allow_html=True)
    if 'image_paths' in st.session_state:
        with st.spinner("Generating sounds..."):
            st.session_state.sound_paths = create_audio_files(st.session_state.story_scenes)

        for i, sound_path in enumerate(st.session_state.sound_paths.values(), start=1):
            st.audio(sound_path)
            track_temp_dir(os.path.dirname(sound_path))
        st.session_state.selected_tab = 'Get Your Video'
    else:
        st.write("Please go back and preview the images first.")


elif st.session_state['selected_tab'] == 'Get Your Video':
    st.markdown("<h2 style='text-align: center;'>Final Step: Get Your Video</h2>", unsafe_allow_html=True)
    if 'sound_paths' in st.session_state:
        with st.spinner("Generating video..."):
            videos_gameplay = {
                "minecraft": "./gameplay_folder\\minecraft_1.mp4",
                "car": "./gameplay_folder\\car_runner_1.mp4",
                "cycling": "./gameplay_folder\\cycling_1.mp4"
            }
            selected_style, game_video_play_path = random.choice(list(videos_gameplay.items()))
            logging.info(selected_style)
            video_path = create_video_without_captions(st.session_state.image_paths, st.session_state.sound_paths, game_video_play_path)
            st.session_state.video_path = video_path
            track_temp_dir(os.path.dirname(video_path))
            logging.info("Main Video Completed")
        with st.spinner("Adding fancy captions..."):
            final_video_path = add_fancy_captions(video_path, st.session_state.story_scenes, st.session_state.sound_paths)

            st.session_state.final_video_path = final_video_path
            st.success("Your video is ready!")
            track_temp_dir(os.path.dirname(final_video_path))
            logging.info("Final Video Successfully Generated")
            logging.info(st.session_state.temporary_files)

        st.video(st.session_state.final_video_path, autoplay=True)
        st.write("Before Clicking Button Make Sure to download the video from three dots at bottom right corner in Video Editor")

    else:
        st.write("Please go back and preview the sounds first.")

    if st.button("Cleanup File and Move to Home Page"):
        cleanup_temp_files()
        st.session_state.selected_tab = 'Home'


st.sidebar.markdown("---")
st.sidebar.write("Thank you for using Reelify AI created by Keshav!")
