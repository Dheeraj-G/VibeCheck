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
            
            song_id = data.get("songId")
            user_token = data.get("userToken")
            
            logger.info(f"[RECV] /recommendations called. songId: {song_id}")
            
            if not song_id:
                logger.warning("[ERROR] No songId provided in request body.")
                self.send_error_response(400, {"error": "songId required"})
                return
            
            if not engine:
                logger.error("[ERROR] Engine unavailable.")
                self.send_error_response(503, {"error": "Engine unavailable"})
                return
            
            result = engine.get_recommendations(selected_song_id=song_id, user_token=user_token)
            logger.info(f"[SEND] Recommendations response: {json.dumps(result.get('songs', []), indent=2)}")
            
            status_code = 200 if result.get("success", False) else 500
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            logger.error(f"Error in /recommendations: {e}")
            self.send_error_response(500, {"error": "Internal server error"})
    
    def send_error_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
