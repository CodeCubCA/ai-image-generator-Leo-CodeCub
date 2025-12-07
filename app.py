import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
import random

# Load environment variables
load_dotenv()

# Configuration
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Random prompts for inspiration
RANDOM_PROMPTS = [
    "A cyberpunk city at sunset, neon lights, futuristic architecture",
    "A magical forest with glowing mushrooms, ethereal lighting, fantasy art",
    "A cute robot reading a book in a library, warm lighting, detailed",
    "An astronaut riding a horse on Mars, cinematic, epic scene",
    "A steampunk airship flying over mountains, dramatic clouds, vintage",
    "A cat wearing a wizard hat casting spells, digital art, whimsical",
    "A futuristic sports car in a neon tunnel, motion blur, sci-fi",
    "A cozy treehouse in autumn, warm lighting, peaceful atmosphere",
    "A dragon sleeping on a pile of books, fantasy art, detailed scales",
    "An underwater city with bioluminescent plants, mysterious, deep ocean",
    "A coffee shop on a rainy day, cozy interior, warm colors",
    "A phoenix rising from flames, majestic, vibrant colors",
    "A samurai warrior in a cherry blossom garden, cinematic lighting",
    "A Victorian mansion at night, gothic atmosphere, moonlight",
    "A whale swimming through clouds, surreal, dreamlike"
]

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 20px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        height: 3em;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #145a8c;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🎨 AI Image Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Generate stunning images from text using AI</p>", unsafe_allow_html=True)

# Check if API token is configured
if not HUGGINGFACE_TOKEN or HUGGINGFACE_TOKEN == "your_token_here":
    st.error("⚠️ HuggingFace API token not configured!")
    st.info("""
    **Setup Instructions:**
    1. Go to https://huggingface.co/settings/tokens
    2. Create a new token with **Write** permissions
    3. Copy the token
    4. Create a `.env` file in the project directory
    5. Add: `HUGGINGFACE_TOKEN=your_token_here`
    6. Restart the application
    """)
    st.stop()

# Initialize the HuggingFace Inference Client
@st.cache_resource
def get_inference_client():
    """Initialize and cache the HuggingFace Inference Client"""
    try:
        return InferenceClient(token=HUGGINGFACE_TOKEN)
    except Exception as e:
        st.error(f"Failed to initialize HuggingFace client: {str(e)}")
        return None

client = get_inference_client()

if not client:
    st.stop()

# Main interface
st.markdown("---")

# Initialize prompt in session state
if 'prompt_value' not in st.session_state:
    st.session_state['prompt_value'] = ""

# Random Prompt button
if st.button("🎲 Random Prompt", help="Get a random creative prompt for inspiration!"):
    st.session_state['prompt_value'] = random.choice(RANDOM_PROMPTS)

# Input section
prompt = st.text_area(
    "Enter your image description:",
    value=st.session_state['prompt_value'],
    placeholder="Example: A serene landscape with mountains at sunset, photorealistic, 4k",
    height=100,
    help="Describe the image you want to generate. Be specific for better results!"
)

# Update session state with any user changes
st.session_state['prompt_value'] = prompt

# Negative prompt input
negative_prompt = st.text_input(
    "Negative Prompt (Optional)",
    placeholder="What you DON'T want in the image...",
    help="Examples: 'blurry, low quality, distorted' or 'dark, gloomy, scary' or 'text, watermark, signature'"
)

# Image size selection
st.markdown("**Image Size:**")
size_options = {
    "Square (512x512)": (512, 512),
    "Portrait (512x768)": (512, 768),
    "Landscape (768x512)": (768, 512)
}

selected_size = st.selectbox(
    "Choose image dimensions",
    options=list(size_options.keys()),
    index=0,
    help="Select the aspect ratio for your generated image",
    label_visibility="collapsed"
)

width, height = size_options[selected_size]

# Advanced options (collapsible)
with st.expander("⚙️ Advanced Options"):
    st.info(f"**Current Model:** {MODEL_NAME}")
    st.caption("This model is optimized for fast, high-quality image generation.")

    st.markdown("**Negative Prompt Examples:**")
    st.caption("• `blurry, low quality, distorted, deformed`")
    st.caption("• `dark, gloomy, scary, horror`")
    st.caption("• `text, watermark, signature, logo`")
    st.caption("• `ugly, bad anatomy, poorly drawn`")

# Generate button
if st.button("✨ Generate Image"):
    if not prompt.strip():
        st.warning("⚠️ Please enter a description for your image.")
    else:
        try:
            # Show loading state
            with st.spinner("🎨 Creating your image... This may take 10-30 seconds..."):
                # Prepare parameters for image generation
                generation_params = {
                    "prompt": prompt,
                    "model": MODEL_NAME,
                    "width": width,
                    "height": height
                }

                # Add negative prompt if provided
                if negative_prompt.strip():
                    generation_params["negative_prompt"] = negative_prompt

                # Generate image using InferenceClient
                image = client.text_to_image(**generation_params)

                # Store in session state
                st.session_state['generated_image'] = image
                st.session_state['last_prompt'] = prompt
                st.session_state['last_size'] = selected_size
                if negative_prompt.strip():
                    st.session_state['last_negative_prompt'] = negative_prompt

            st.success("✅ Image generated successfully!")

        except Exception as e:
            error_message = str(e)

            # Handle specific error cases
            if "rate limit" in error_message.lower():
                st.error("⚠️ **Rate limit exceeded!**")
                st.info("The free tier has limits. Please wait a few minutes and try again.")
            elif "authorization" in error_message.lower() or "unauthorized" in error_message.lower():
                st.error("⚠️ **Authentication failed!**")
                st.info("""
                Your API token may be invalid or expired. Please check:
                1. Token has **Write** permissions (read-only tokens don't work)
                2. Token is correctly copied to your `.env` file
                3. You've restarted the application after updating `.env`
                """)
            elif "model" in error_message.lower():
                st.error("⚠️ **Model error!**")
                st.info("The model may be unavailable. This usually resolves itself quickly.")
            else:
                st.error(f"⚠️ **Error generating image:** {error_message}")
                st.info("Please try again or try a different prompt.")

# Display section
st.markdown("---")

if 'generated_image' in st.session_state:
    st.subheader("Generated Image")

    # Build caption with prompt, size, and negative prompt if used
    caption_text = f"Prompt: {st.session_state['last_prompt']}"
    if 'last_size' in st.session_state:
        caption_text += f"\nSize: {st.session_state['last_size']}"
    if 'last_negative_prompt' in st.session_state:
        caption_text += f"\nNegative Prompt: {st.session_state['last_negative_prompt']}"

    # Display the image
    st.image(
        st.session_state['generated_image'],
        caption=caption_text,
        use_container_width=True
    )

    # Download button
    # Convert PIL Image to bytes for download
    from io import BytesIO

    buf = BytesIO()
    st.session_state['generated_image'].save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="⬇️ Download Image",
        data=byte_im,
        file_name="generated_image.png",
        mime="image/png"
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Powered by <a href='https://huggingface.co/' target='_blank'>HuggingFace</a> 🤗</p>
        <p style='font-size: 12px;'>Model: FLUX.1-schnell by Black Forest Labs</p>
    </div>
    """, unsafe_allow_html=True)
