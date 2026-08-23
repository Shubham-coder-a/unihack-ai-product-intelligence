import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Supported Groq Models
AVAILABLE_MODELS = {
    "Llama 3.3 70B Versatile (Recommended)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B Instant (Ultra-Fast)": "llama-3.1-8b-instant",
    "Mixtral 8x7b": "mixtral-8x7b-32768",
    "DeepSeek R1 Distill Llama 70B": "deepseek-r1-distill-llama-70b",
}

DEFAULT_MODEL = "llama-3.3-70b-versatile"
