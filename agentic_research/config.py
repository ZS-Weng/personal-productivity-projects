# config.py - Settings and model selection

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

#CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Model selection
DEFAULT_MODEL = "gemini"  # or "claude"

# Other settings
MAX_TOKENS = 1000
TEMPERATURE = 0.7