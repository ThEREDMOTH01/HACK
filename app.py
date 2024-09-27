import os
import openai
import streamlit as st
from dotenv import load_dotenv
import moviepy.editor as mpy
import requests

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a story using OpenAI's API
def generate_story(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Function to call an image generation API (you can replace this with your actual image generation logic)
def generate_image(prompt):
    # Placeholder for image generation logic
    return f"{prompt.replace(' ', '_')}.jpg"  # Simulating image generation

# Function to create video from images
def create_video(image_files, output_file):
    clips = [mpy.ImageClip(img).set_duration(2) for img in image_files if img is not None]
    if clips:
        video = mpy.concatenate_videoclips(clips, method="compose")
        video.write_videofile(output_file, fps=24)
    else:
        st.error("No images to create video.")

# Streamlit UI
st.title("Text to Video Generation with OpenAI")
story_prompt = st.text_area("Enter your story prompt:", height=150)

if st.button("Generate Story and Video"):
    # Step 1: Generate story
    generated_story = generate_story(story_prompt)
    st.subheader("Generated Story")
    st.write(generated_story)
    
    # Step 2: Generate images based on story sentences
    image_files = []
    for sentence in generated_story.split('.'):
        if sentence.strip():
            img_file = generate_image(sentence.strip())
            image_files.append(img_file)  # Simulating image generation
    
    # Step 3: Create video from images
    output_video_file = "output_video.mp4"
    create_video(image_files, output_video_file)
    
    # Step 4: Provide download link for video
    st.video(output_video_file)
    st.success("Video generated successfully!")
