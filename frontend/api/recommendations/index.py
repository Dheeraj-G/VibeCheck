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
    def do_GET(self):
        if self.path == '/health':
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
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/track':
            self.handle_track_info()
        elif self.path == '/recommendations':
            self.handle_recommendations()
        elif self.path == '/prompt_recommendations':
            self.handle_prompt_recommendations()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_track_info(self):
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
    
    def handle_recommendations(self):
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
    
    def handle_prompt_recommendations(self):
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
