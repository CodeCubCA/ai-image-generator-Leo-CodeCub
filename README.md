[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zrsH8x_3)

# AI Image Generator

A web application that generates images from text descriptions using HuggingFace's Inference API and Streamlit.

## Features

- Simple and intuitive web interface
- Text-to-image generation using FLUX.1-schnell model
- Real-time loading indicators
- Download generated images
- Error handling for API failures and rate limits

## Prerequisites

- Python 3.8 or higher
- HuggingFace account and API token

## Setup Instructions

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

The app will open in your browser at `http://localhost:8501`

## Usage

1. Enter a description of the image you want to generate
2. Click "Generate Image"
3. Wait 10-30 seconds for the image to generate
4. Download the image if desired

## Example Prompts

- "A serene landscape with mountains at sunset, photorealistic, 4k"
- "A cute robot painting on a canvas, digital art"
- "An astronaut riding a horse on Mars, cinematic lighting"
- "A cozy coffee shop interior, warm lighting, detailed"

## Troubleshooting

### Authentication Error
- Make sure your token has **Write** permissions (not just Read)
- Verify the token is correctly copied to `.env`
- Restart the application after updating `.env`

### Rate Limit Error
- Free tier has usage limits
- Wait a few minutes before trying again
- Consider upgrading your HuggingFace account for higher limits

### Model Unavailable
- The model may be temporarily unavailable
- Try again in a few minutes
- Check [HuggingFace Status](https://status.huggingface.co/)

## Technical Details

- **Frontend**: Streamlit
- **AI Model**: FLUX.1-schnell by Black Forest Labs
- **API**: HuggingFace Inference API via `huggingface_hub` library
- **Image Processing**: Pillow (PIL)

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

## License

This project is for educational purposes as part of CodeCub CA's curriculum.

## Credits

- Built with [Streamlit](https://streamlit.io/)
- Powered by [HuggingFace](https://huggingface.co/)
- Model: FLUX.1-schnell by Black Forest Labs
