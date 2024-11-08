import os
import uuid
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_video_without_captions(images_path, audio_paths, gameplay_video_path):

    temp_dir = os.path.join('./', str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)

    scenes = []
    scene_mapping = {f"prompt_{i + 1}": f"scene_{i + 1}" for i in range(len(images_path))}

    for image_key, scene_key in scene_mapping.items():
        logging.info(f"Processing {scene_key}")
        image_files = images_path[image_key]
        audio_file = audio_paths[scene_key]

        combined_image_clips = [ImageClip(img).set_duration(AudioFileClip(audio_file).duration / 2).crossfadein(1) for img in image_files]
        combined_scene = concatenate_videoclips(combined_image_clips, method="compose")
        audio_clip = AudioFileClip(audio_file)
        scene_with_audio = combined_scene.set_audio(audio_clip)
        scenes.append(scene_with_audio)

    logging.info("Final Step")
    main_video = concatenate_videoclips(scenes)
    main_video_path = os.path.join(temp_dir, "main_video.mp4")
    main_video.write_videofile(main_video_path, codec="libx264", fps=24)

    gameplay_clip = VideoFileClip(gameplay_video_path).subclip(0, main_video.duration).without_audio()
    gameplay_clip_resized = gameplay_clip.resize((main_video.w, main_video.h))

    logging.info("Creating final split screen video")
    final_video = CompositeVideoClip([
        main_video.set_position(("center", "top")),
        gameplay_clip_resized.set_position(("center", "bottom"))
    ], size=(main_video.w, main_video.h * 2))

    final_video_path = os.path.join(temp_dir, "final_video.mp4")
    final_video.write_videofile(final_video_path, codec="libx264", fps=24)

    return final_video_path

