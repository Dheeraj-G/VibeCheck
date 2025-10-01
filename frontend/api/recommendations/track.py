from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import logging

# Add the parent directory to the path to find song_recommendations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from song_recommendations import SongRecommendationsEngine

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
            
            track_id = data.get("trackId")
            if not track_id:
                self.send_error_response(400, {"error": "trackId required"})
                return
            
            track_info = engine.get_track_info(track_id)
            self.send_success_response(track_info)
            
        except Exception as e:
            logger.error(f"Error in /track: {e}")
            self.send_error_response(500, {"error": "Internal server error"})
    
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
