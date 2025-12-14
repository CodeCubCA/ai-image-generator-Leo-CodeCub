import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
import random
from datetime import datetime

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

# Style presets
STYLE_PRESETS = {
    "None": "",
    "Anime": ", anime style, vibrant colors, Studio Ghibli inspired, detailed illustration, hand-drawn",
    "Realistic": ", photorealistic, highly detailed, 8K resolution, professional photography, sharp focus",
    "Digital Art": ", digital painting, trending on artstation, concept art, smooth, sharp focus, illustration",
    "Watercolor": ", watercolor painting, soft colors, artistic, flowing, delicate, hand-painted",
    "Oil Painting": ", oil painting, classical art, textured brushstrokes, canvas, museum quality",
    "Cyberpunk": ", cyberpunk style, neon lights, futuristic, sci-fi, dystopian, high-tech",
    "Fantasy": ", fantasy art, magical, enchanted, epic, mythical, ethereal, dramatic lighting"
}

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

# Initialize image history in session state
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Sidebar for style presets
with st.sidebar:
    st.header("🎨 Style Presets")

    selected_style = st.selectbox(
        "Choose a style:",
        options=list(STYLE_PRESETS.keys()),
        index=0,
        help="Select a style to automatically enhance your prompt with style-specific keywords"
    )

    # Show style description
    if selected_style != "None":
        st.caption(f"**Style adds:** {STYLE_PRESETS[selected_style].strip(', ')}")
    else:
        st.caption("Using your original prompt without style modifications")

    st.markdown("---")
    st.markdown("**About Styles:**")
    st.caption("Styles automatically add keywords to enhance your prompt and create consistent results.")

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
            # Apply style preset to prompt
            enhanced_prompt = prompt + STYLE_PRESETS[selected_style]

            # Show enhanced prompt if style is applied
            if selected_style != "None":
                with st.expander("📝 Enhanced Prompt Preview"):
                    st.text(enhanced_prompt)

            # Show loading state
            with st.spinner("🎨 Creating your image... This may take 10-30 seconds..."):
                # Prepare parameters for image generation
                generation_params = {
                    "prompt": enhanced_prompt,
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
                st.session_state['last_enhanced_prompt'] = enhanced_prompt
                st.session_state['last_style'] = selected_style
                st.session_state['last_size'] = selected_size
                if negative_prompt.strip():
                    st.session_state['last_negative_prompt'] = negative_prompt

                # Add to image history
                image_data = {
                    'image': image,
                    'prompt': prompt,
                    'enhanced_prompt': enhanced_prompt,
                    'style': selected_style,
                    'size': selected_size,
                    'negative_prompt': negative_prompt if negative_prompt.strip() else None,
                    'timestamp': datetime.now()
                }
                st.session_state.image_history.insert(0, image_data)

                # Limit history to 10 images
                if len(st.session_state.image_history) > 10:
                    st.session_state.image_history = st.session_state.image_history[:10]

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

    # Build caption with prompt, style, size, and negative prompt if used
    caption_text = f"Prompt: {st.session_state['last_prompt']}"
    if 'last_style' in st.session_state and st.session_state['last_style'] != "None":
        caption_text += f"\nStyle: {st.session_state['last_style']}"
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

    # Show full enhanced prompt in expander
    if 'last_enhanced_prompt' in st.session_state and st.session_state.get('last_style') != "None":
        with st.expander("📝 View Full Prompt Used"):
            st.text(st.session_state['last_enhanced_prompt'])

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

# Image History Gallery
st.markdown("---")
st.markdown("---")

if len(st.session_state.image_history) > 0:
    # Header with count and clear button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(f"📸 Image History ({len(st.session_state.image_history)} images)")
    with col2:
        if st.button("🗑️ Clear History", help="Delete all images from history"):
            st.session_state.image_history = []
            st.rerun()

    st.caption("Your most recent images from this session (max 10)")
    st.markdown("---")

    # Display images in grid (3 columns)
    for i in range(0, len(st.session_state.image_history), 3):
        cols = st.columns(3)

        for j in range(3):
            idx = i + j
            if idx < len(st.session_state.image_history):
                img_data = st.session_state.image_history[idx]

                with cols[j]:
                    # Display image
                    st.image(img_data['image'], use_container_width=True)

                    # Display prompt (truncated)
                    prompt_text = img_data['prompt']
                    if len(prompt_text) > 50:
                        with st.expander("View Prompt"):
                            st.text(prompt_text)
                    else:
                        st.caption(f"**Prompt:** {prompt_text}")

                    # Show style if not None
                    if img_data['style'] != "None":
                        st.caption(f"🎨 {img_data['style']}")

                    # Download button for each image
                    from io import BytesIO
                    buf = BytesIO()
                    img_data['image'].save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    st.download_button(
                        label="⬇️ Download",
                        data=byte_im,
                        file_name=f"generated_{idx+1}.png",
                        mime="image/png",
                        key=f"download_history_{idx}",
                        use_container_width=True
                    )

                    # Regenerate button
                    if st.button("🔄 Regenerate", key=f"regen_{idx}", use_container_width=True, help="Use this prompt again"):
                        st.session_state['prompt_value'] = img_data['prompt']
                        st.rerun()

                    st.markdown("---")

else:
    st.info("📭 No images in history yet. Generate your first image above!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Powered by <a href='https://huggingface.co/' target='_blank'>HuggingFace</a> 🤗</p>
        <p style='font-size: 12px;'>Model: FLUX.1-schnell by Black Forest Labs</p>
    </div>
    """, unsafe_allow_html=True)
