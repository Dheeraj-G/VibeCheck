#!/usr/bin/env python3
"""
Flask server for VibeCheck song recommendations API
Serves as a bridge between the Next.js frontend and the Python recommendations engine
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from song_recommendations import SongRecommendationsEngine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the recommendations engine
try:
    engine = SongRecommendationsEngine()
    logger.info("Song recommendations engine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize recommendations engine: {e}")
    engine = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        groq_status = "unknown"
        selected_model = "none"
        
        if engine and hasattr(engine, 'groq_client'):
            try:
                # Test Groq API connection
                test_response = engine._call_groq_api("test", max_tokens=5)
                groq_status = "connected" if test_response else "error"
                selected_model = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
            except Exception as e:
                groq_status = f"error: {str(e)}"
        
        return jsonify({
            'status': 'healthy',
            'engine_available': engine is not None,
            'groq_status': groq_status,
            'selected_model': selected_model
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/search', methods=['GET'])
def search_songs():
    """Search for songs on Spotify"""
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        if not engine:
            return jsonify({'error': 'Recommendations engine not available'}), 503
        
        songs = engine.search_songs(query, limit)
        return jsonify({
            'success': True,
            'songs': songs,
            'query': query
        })
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get song recommendations based on prompt and optional selected song"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        prompt = data.get('prompt', '')
        selected_song = data.get('selectedSong')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        if not engine:
            return jsonify({'error': 'Recommendations engine not available'}), 503
        
        # Get recommendations
        result = engine.get_recommendations(prompt, selected_song)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/song-features/<song_id>', methods=['GET'])
def get_song_features(song_id):
    """Get audio features for a specific song"""
    try:
        if not engine:
            return jsonify({'error': 'Recommendations engine not available'}), 503
        
        features = engine.get_song_features(song_id)
        
        if features:
            return jsonify({
                'success': True,
                'song_id': song_id,
                'features': features
            })
        else:
            return jsonify({'error': 'Song features not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting song features: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/similar-songs/<song_id>', methods=['GET'])
def get_similar_songs(song_id):
    """Get similar songs based on a seed track"""
    try:
        limit = int(request.args.get('limit', 5))
        
        if not engine:
            return jsonify({'error': 'Recommendations engine not available'}), 503
        
        similar_songs = engine.get_similar_songs_by_features(song_id, limit)
        
        return jsonify({
            'success': True,
            'seed_song_id': song_id,
            'songs': similar_songs
        })
        
    except Exception as e:
        logger.error(f"Error getting similar songs: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/ollama/models', methods=['GET'])
def get_ollama_models():
    """Get available Ollama models"""
    try:
        if not engine or not hasattr(engine, 'ollama_client'):
            return jsonify({'error': 'Ollama client not available'}), 503
        
        models = engine.ollama_client.list()
        return jsonify({
            'success': True,
            'models': models['models'],
            'selected_model': getattr(engine, 'selected_model', 'none')
        })
        
    except Exception as e:
        logger.error(f"Error getting Ollama models: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/ollama/download/<model_name>', methods=['POST'])
def download_ollama_model(model_name):
    """Download a specific Ollama model"""
    try:
        if not engine or not hasattr(engine, 'ollama_client'):
            return jsonify({'error': 'Ollama client not available'}), 503
        
        # Validate model name
        valid_models = ['llama3.1:8b', 'llama3.1:70b', 'llama3:8b', 'llama3:70b']
        if model_name not in valid_models:
            return jsonify({'error': f'Invalid model. Valid models: {valid_models}'}), 400
        
        logger.info(f"Downloading Ollama model: {model_name}")
        
        # Download the model
        engine.ollama_client.pull(model_name)
        
        # Refresh model list
        models = engine.ollama_client.list()
        available_models = [model['name'] for model in models['models']]
        
        if model_name in available_models:
            # Update selected model
            engine.selected_model = model_name
            return jsonify({
                'success': True,
                'message': f'Successfully downloaded {model_name}',
                'selected_model': model_name
            })
        else:
            return jsonify({'error': f'Failed to download {model_name}'}), 500
            
    except Exception as e:
        logger.error(f"Error downloading Ollama model: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Configuration
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Check if required environment variables are set
    required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Some features may not work properly")
    
    logger.info(f"Starting VibeCheck recommendations server on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        exit(1)
