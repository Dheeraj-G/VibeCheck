from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from song_recommendations import SongRecommendationsEngine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize engine globally
try:
    engine = SongRecommendationsEngine()
except Exception as e:
    logger.error(f"Failed to initialize recommendations engine: {e}")
    engine = None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "healthy",
            "engine_available": engine is not None,
            "spotify_connected": engine.spotify_client is not None if engine else False
        }
        self.wfile.write(json.dumps(response).encode())
