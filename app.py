import requests
import io
from PIL import Image
import streamlit as st

# Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HEADERS = {"Authorization": "Bearer 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"}  # Replace with your API key

# Streamlit UI elements
st.set_page_config(page_title="AI Image Generator", page_icon="🎨", layout="wide")

# Title & Header
st.title("AI Image Generator 🎨")
st.markdown("""
    This application uses Stable Diffusion to generate images based on text prompts.
    Enter a text prompt and click 'Generate Image' to see the magic!
""")
st.sidebar.title("Settings")

# Sidebar for additional options
with st.sidebar:
    st.header("Configuration")
    prompt_placeholder = "e.g., A sunset over the mountains"
    style = st.selectbox("Select Style", ["Realistic", "Abstract", "Fantasy", "Cyberpunk"])
    img_size = st.slider("Image Size", 256, 1024, 512, step=128, help="Select the resolution of the generated image.")
    st.markdown("###")

# Take user input
prompt = st.text_input("Enter your prompt", placeholder=prompt_placeholder)

# Send request to API
def generate_image(prompt, style, img_size):
    # Construct the payload based on the selected style and image size
    payload = {"inputs": f"{style} {prompt}", "parameters": {"size": img_size}}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        return image
    else:
        st.error(f"Error generating image: {response.text}")
        return None

# When the user clicks the button, generate and display the image
if st.button("Generate Image") and prompt:
    with st.spinner("Generating image..."):
        # Show a progress bar while generating
        progress = st.progress(0)
        for i in range(1, 101, 20):
            progress.progress(i)
        image = generate_image(prompt, style, img_size)
        if image:
            st.image(image, caption=f"Generated Image ({style} style)", use_column_width=True)
        progress.progress(100)  # Complete progress bar

else:
    st.markdown("""
    **Tips:**
    - Enter a descriptive text prompt.
    - You can select a style or leave it as the default.
    - Adjust the image resolution for higher-quality results.
    """)
