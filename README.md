---
title: AI Image Generator
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.31.0"
app_file: app.py
pinned: false
---

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zrsH8x_3)

# 🎨 AI Image Generator

A professional web application that generates stunning AI images from text descriptions using HuggingFace's FLUX.1-schnell model and Streamlit.

Transform your ideas into beautiful images with just a few words!

## ✨ Features

### Core Functionality
- **Text-to-Image Generation**: Create images from natural language descriptions using FLUX.1-schnell AI model
- **Style Presets**: 8 professional style options including:
  - Anime (Studio Ghibli inspired)
  - Realistic (8K photorealistic)
  - Digital Art (Artstation quality)
  - Watercolor
  - Oil Painting
  - Cyberpunk
  - Fantasy
- **Image History Gallery**: View and manage up to 10 recently generated images
- **Random Prompt Generator**: Get instant creative inspiration with pre-made prompts
- **Negative Prompts**: Specify what you DON'T want in your images for better results
- **Multiple Image Sizes**: Choose between Square, Portrait, or Landscape formats
- **Download Functionality**: Save any generated image with one click
- **Regenerate Feature**: Quickly recreate images with the same settings

### User Experience
- Clean, intuitive interface
- Real-time loading indicators
- Comprehensive error handling
- Responsive design
- Session-based image history

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **HuggingFace Inference API**: AI model access
- **FLUX.1-schnell**: State-of-the-art text-to-image model by Black Forest Labs
- **Pillow (PIL)**: Image processing
- **python-dotenv**: Environment variable management

## 📋 Prerequisites

- Python 3.8 or higher
- HuggingFace account (free)
- HuggingFace API token with Write permissions

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/CodeCubCA/ai-image-generator-Leo-Codecub.git
cd ai-image-generator-Leo-Codecub
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get HuggingFace API Token

1. Go to [HuggingFace Settings - Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name (e.g., "image-generator")
4. Select **"Write"** permissions (important - read-only tokens won't work!)
5. Click "Generate token"
6. Copy the token (it starts with `hf_`)

### 5. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and add your HuggingFace token:
   ```
   HUGGINGFACE_TOKEN=hf_your_actual_token_here
   ```

### 6. Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 💡 How to Use

### Basic Workflow
1. **Select a Style** (optional): Choose from 8 preset styles in the sidebar
2. **Enter a Prompt**: Describe the image you want to create
3. **Add Negative Prompt** (optional): Specify what to avoid (e.g., "blurry, low quality")
4. **Choose Image Size**: Select Square, Portrait, or Landscape
5. **Generate**: Click the "Generate Image" button
6. **Download**: Save your creation with the download button

### Pro Tips
- Use the **🎲 Random Prompt** button for creative inspiration
- Check **Image History** to view all generated images from your session
- Use the **🔄 Regenerate** button to recreate images with the same settings
- Combine style presets with detailed prompts for best results

## 🎨 Example Prompts

**Landscapes:**
- "A serene mountain lake at sunset, surrounded by pine trees, golden hour lighting"
- "Futuristic city skyline at night, neon lights reflecting on wet streets"

**Characters:**
- "A friendly robot reading a book in a cozy library, warm lighting"
- "Astronaut floating in space near a colorful nebula, cinematic"

**Abstract/Artistic:**
- "Abstract representation of music, flowing colors and shapes"
- "Steampunk coffee machine with brass gears and steam, detailed"

## ⚠️ Troubleshooting

### Authentication Error
- Ensure your token has **Write** permissions (read-only tokens won't work)
- Verify the token is correctly copied to `.env` file
- Restart the application after updating `.env`
- Check token validity at [HuggingFace Settings](https://huggingface.co/settings/tokens)

### Rate Limit Error
- Free tier has usage limits on API calls
- Wait a few minutes before trying again
- Consider upgrading your HuggingFace account for higher limits
- Spread out your generation requests

### Model Unavailable
- The model may be temporarily unavailable
- Try again in a few minutes
- Check [HuggingFace Status](https://status.huggingface.co/)

### Image Not Generating
- Ensure your prompt is descriptive and clear
- Try using a style preset for better results
- Check your internet connection
- Verify HuggingFace API is accessible

## 📊 Technical Architecture

**Frontend:**
- Streamlit web framework
- Session state management for image history
- Responsive UI with sidebar controls

**Backend:**
- HuggingFace Inference API integration
- FLUX.1-schnell model by Black Forest Labs
- PIL/Pillow for image processing
- Environment-based configuration

## Project Structure

```
ai-image-generator/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not tracked)
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🎯 Future Enhancements

Potential features for future versions:
- Image-to-image editing
- Batch image generation
- Save/load custom style presets
- Share images directly to social media
- Export generation history
- Advanced parameter controls (seed, steps, guidance)

## 📝 License

This project is for educational purposes as part of CodeCub CA's curriculum.

## 🙏 Credits & Acknowledgments

- **Framework**: Built with [Streamlit](https://streamlit.io/)
- **AI Platform**: Powered by [HuggingFace](https://huggingface.co/)
- **AI Model**: FLUX.1-schnell by [Black Forest Labs](https://blackforestlabs.ai/)
- **Educational Program**: [CodeCub CA](https://codecub.ca/)

## 📫 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the Troubleshooting section above
- Review HuggingFace documentation

---

**Made with ❤️ using AI and Python**
