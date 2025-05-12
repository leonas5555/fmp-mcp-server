import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for FMP MCP server."""
    
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    if not FMP_API_KEY:
        raise ValueError("FMP_API_KEY environment variable not set")

    # Server config
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8080"))

config = Config()
