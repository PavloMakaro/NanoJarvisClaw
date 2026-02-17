import os
import requests
import yt_dlp
from openai import OpenAI
import config
import base64

def register_tools(registry):
    registry.register("download_video", download_video, "Downloads a video. Arguments: url (str). Returns filepath.")
    registry.register("transcribe_audio", transcribe_audio, "Transcribes audio file. Arguments: filepath (str).")
    registry.register("recognize_image", recognize_image, "Recognizes text in an image using OCR.Space. Arguments: filepath (str).")
    registry.register("recognize_image_groq", recognize_image_groq, "Recognizes text/content in an image using Groq Vision. Arguments: filepath (str).")

def download_video(url):
    """Downloads a video using yt-dlp."""
    try:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return f"Video downloaded to: {filename}"

    except Exception as e:
        return f"Error downloading video: {str(e)}"

def transcribe_audio(filepath):
    """Transcribes audio using Groq Whisper."""
    try:
        client = OpenAI(
            api_key=config.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        if not os.path.exists(filepath):
            return "Error: File not found."

        with open(filepath, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(filepath), file.read()),
                model="whisper-large-v3",
                response_format="text"
            )
        return transcription
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def recognize_image(filepath):
    """Recognizes text in an image using OCR.Space."""
    try:
        if not os.path.exists(filepath):
            return "Error: File not found."

        payload = {
            'apikey': config.OCR_API_KEY,
            'language': 'eng',
            'isOverlayRequired': False
        }

        with open(filepath, 'rb') as f:
            r = requests.post(
                'https://api.ocr.space/parse/image',
                files={'file': f},
                data=payload,
                timeout=20
            )

        result = r.json()
        if result.get('IsErroredOnProcessing'):
            return f"OCR Error: {result.get('ErrorMessage')}"

        parsed_results = result.get('ParsedResults', [])
        if not parsed_results:
            return "No text found."

        text = parsed_results[0].get('ParsedText')
        return text
    except Exception as e:
        return f"Error recognizing image: {str(e)}"

def recognize_image_groq(filepath):
    """Recognizes content in an image using Groq Vision (llama-3.2-11b-vision-preview)."""
    try:
        if not os.path.exists(filepath):
            return "Error: File not found."

        client = OpenAI(
            api_key=config.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(filepath)

        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in detail and extract any text found."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        return completion.choices[0].message.content
    except Exception as e:
        return f"Error with Groq Vision: {str(e)}"
