import os
import openai
import streamlit as st
from dotenv import load_dotenv
import moviepy.editor as mpy

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a story using OpenAI's API
def generate_story(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Error generating story: {str(e)}")
        return None

# Function to simulate image generation (replace this with your actual image generation logic)
def generate_image(prompt):
    # Placeholder: In a real scenario, you would call your image generation logic/API here
    # For now, it will simulate image generation by returning a placeholder image
    return f"{prompt.replace(' ', '_')}.jpg"  # Simulating image generation

# Function to create video from images
def create_video(image_files, output_file):
    clips = []
    for img in image_files:
        if os.path.exists(img):  # Check if the image file exists
            clips.append(mpy.ImageClip(img).set_duration(2))
        else:
            st.warning(f"Image file {img} does not exist.")
    
    if clips:
        video = mpy.concatenate_videoclips(clips, method="compose")
        video.write_videofile(output_file, fps=24)
    else:
        st.error("No valid images to create video.")

# Streamlit UI
st.title("Text to Video Generation")
scene_prompts = st.text_area("Enter scene prompts (one per line):", height=150)

if st.button("Generate Video"):
    if not scene_prompts:
        st.error("Please enter at least one scene prompt.")
    else:
        # Split prompts into a list
        prompts = scene_prompts.splitlines()
        
        # Generate images based on scene prompts
        image_files = []
        for prompt in prompts:
            if prompt.strip():
                img_file = generate_image(prompt.strip())
                image_files.append(img_file)  # Simulating image generation
        
        # Create video from images
        output_video_file = "output_video.mp4"
        create_video(image_files, output_video_file)

        # Provide download link for video
        if os.path.exists(output_video_file):
            st.video(output_video_file)
            st.success("Video generated successfully!")
        else:
            st.error("Video generation failed.")
