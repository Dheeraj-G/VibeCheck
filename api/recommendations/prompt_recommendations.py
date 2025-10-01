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
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            prompt = data.get("prompt")
            user_token = data.get("userToken")
            
            logger.info(f"[RECV] /prompt_recommendations called. prompt: {prompt}")
            
            if not prompt:
                self.send_error_response(400, {"success": False, "error": "prompt required"})
                return
            
            if not engine:
                self.send_error_response(503, {"success": False, "error": "Engine unavailable"})
                return
            
            genre = engine._genre_from_prompt_via_groq(prompt)
            if not genre:
                self.send_error_response(500, {"success": False, "error": "Could not derive genre from prompt"})
                return
            
            artists = engine.find_artists_by_genre(genre, user_token=user_token, limit=6)
            if not artists:
                self.send_error_response(404, {"success": False, "error": f"No artists found for genre '{genre}'"})
                return
            
            result = {
                "success": True,
                "genre": genre,
                "artists": artists,
                "selected": artists[0]
            }
            
            logger.info(f"[SEND] Prompt recommendations response: {json.dumps(result, indent=2)[:400]}...")
            self.send_success_response(result)
            
        except Exception as e:
            logger.error(f"Error in /prompt_recommendations: {e}")
            self.send_error_response(500, {"success": False, "error": "Internal server error"})
    
    def send_success_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
