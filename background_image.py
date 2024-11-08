import base64
import streamlit as st


def set_background(image_file):
    with open(image_file, "rb") as image:
        b64_image = base64.b64encode(image.read()).decode()  # Encode image to base64 format

    background_style = f"""
    <style>
    .stApp {{
        background: url("data:image/jpeg;base64,{b64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.9;  /* Reduce opacity to make it lighter */
    }}

    /* Add a semi-transparent overlay to lighten the image */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.6);  /* White overlay with 60% opacity */
        z-index: -1;  /* Ensure it stays behind the content */
    }}

    /* Style for the main text to improve readability */
    h1, p, .stMarkdown {{
        color: #333333;  /* Dark text color for visibility */
        font-family: 'Georgia', serif;  /* Custom font */
    }}

    h1 {{
        font-size: 3em;  /* Increase font size for the heading */
        text-align: center;
    }}

    p {{
        font-size: 1.2em;  /* Increase font size for paragraph */
    }}

    .stMarkdown {{
        font-size: 1.2em;  /* Increase font size for markdown content */
        color: #333333;
    }}

    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

