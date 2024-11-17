import cv2
from moviepy.editor import VideoFileClip, AudioFileClip
import logging
import uuid
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_fancy_captions(video_path, captions, audio_paths):
    temp_dir = os.path.join('./', str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)

    output_path = os.path.join(temp_dir, "finished_video.mp4")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    num_scenes = len(captions)

    temp_output_path = os.path.join(temp_dir, "temp_no_audio.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

    current_scene = 0
    word_index = 0
    scene_text = list(captions.values())[current_scene].split()
    pop_up_words = []

    audio_durations = {}
    for scene, audio_path in audio_paths.items():
        audio_clip = AudioFileClip(audio_path)
        audio_durations[scene] = audio_clip.duration

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_time = frame_idx / fps
        if current_time >= (current_scene + 1) * (duration / num_scenes):
            current_scene += 1
            if current_scene < num_scenes:
                scene_text = captions[f"scene_{current_scene + 1}"].split()
                word_index = 0

        scene_id = f"scene_{current_scene + 1}"
        if scene_id in audio_durations:
            scene_duration = audio_durations[scene_id]
            words_in_scene = len(scene_text)
            four_word_interval = scene_duration / (words_in_scene // 4)

        if word_index < len(scene_text):
            if (current_time % four_word_interval) < (1 / fps):
                pop_up_words = scene_text[word_index:word_index + 4]
                word_index += 4

        caption_text = ' '.join(pop_up_words)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.8
        font_thickness = 9
        text_size = cv2.getTextSize(caption_text, font, font_scale, font_thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2

        shadow_color = (0, 0, 0)
        cv2.putText(frame, caption_text, (text_x + 2, text_y + 2), font, font_scale, shadow_color, font_thickness + 2)

        text_color = (255, 255, 255)
        cv2.putText(frame, caption_text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    original_clip = VideoFileClip(video_path)
    captioned_clip = VideoFileClip(temp_output_path)
    captioned_clip = captioned_clip.set_audio(original_clip.audio)
    captioned_clip.write_videofile(output_path, codec="libx264")
    logging.info(f"Video saved as {output_path}")
    return output_path


