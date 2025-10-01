from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from song_recommendations import SongRecommendationsEngine
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize engine
try:
    engine = SongRecommendationsEngine()
except Exception as e:
    logger.error(f"Failed to initialize recommendations engine: {e}")
    engine = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "engine_available": engine is not None,
        "spotify_connected": engine.spotify_client is not None if engine else False
    }), 200

@app.route('/track', methods=['POST'])
def get_track_info():
    """Get track info (name, artist, features)"""
    try:
        data = request.get_json()
        track_id = data.get("trackId")

        if not track_id:
            return jsonify({"error": "trackId required"}), 400

        track_info = engine.get_track_info(track_id)
        return jsonify(track_info), 200
    except Exception as e:
        logger.error(f"Error in /track: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get recommendations from Spotify (song-based only)"""
    try:
        data = request.get_json()
        song_id = data.get("songId")
        user_token = data.get("userToken")  # Get user's Spotify token
        print(f"[INPUT] Received songId: {song_id}")
        logger.info(f"[RECV] /recommendations called. songId: {song_id}")

        if not song_id:
            logger.warning("[ERROR] No songId provided in request body.")
            return jsonify({"error": "songId required"}), 400
        if not engine:
            logger.error("[ERROR] Engine unavailable.")
            return jsonify({"error": "Engine unavailable"}), 503

        result = engine.get_recommendations(selected_song_id=song_id, user_token=user_token)
        logger.info(f"[SEND] Recommendations response: {json.dumps(result.get('songs', []), indent=2)}")
        return jsonify(result), (200 if result.get("success", False) else 500)

    except Exception as e:
        logger.error(f"Error in /recommendations: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/prompt_recommendations', methods=['POST'])
def prompt_recommendations():
    """Get artist recommendations based on a natural language prompt via Groq-derived genre"""
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        user_token = data.get("userToken")
        logger.info(f"[RECV] /prompt_recommendations called. prompt: {prompt}")

        if not prompt:
            return jsonify({"success": False, "error": "prompt required"}), 400
        if not engine:
            return jsonify({"success": False, "error": "Engine unavailable"}), 503

        genre = engine._genre_from_prompt_via_groq(prompt)
        if not genre:
            return jsonify({"success": False, "error": "Could not derive genre from prompt"}), 500

        artists = engine.find_artists_by_genre(genre, user_token=user_token, limit=6)
        if not artists:
            return jsonify({"success": False, "error": f"No artists found for genre '{genre}'"}), 404

        result = {
            "success": True,
            "genre": genre,
            "artists": artists,
            "selected": artists[0]
        }
        logger.info(f"[SEND] Prompt recommendations response: {json.dumps(result, indent=2)[:400]}...")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in /prompt_recommendations: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
