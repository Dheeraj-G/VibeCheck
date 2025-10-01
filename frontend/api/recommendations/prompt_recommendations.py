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

def handler(request):
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        data = json.loads(request.body)
        
        prompt = data.get("prompt")
        user_token = data.get("userToken")
        
        logger.info(f"[RECV] /prompt_recommendations called. prompt: {prompt}")
        
        if not prompt:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'success': False, 'error': 'prompt required'})
            }
        
        if not engine:
            return {
                'statusCode': 503,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'success': False, 'error': 'Engine unavailable'})
            }
        
        genre = engine._genre_from_prompt_via_groq(prompt)
        if not genre:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'success': False, 'error': 'Could not derive genre from prompt'})
            }
        
        artists = engine.find_artists_by_genre(genre, user_token=user_token, limit=6)
        if not artists:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'success': False, 'error': f"No artists found for genre '{genre}'"})
            }
        
        result = {
            "success": True,
            "genre": genre,
            "artists": artists,
            "selected": artists[0]
        }
        
        logger.info(f"[SEND] Prompt recommendations response: {json.dumps(result, indent=2)[:400]}...")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Error in /prompt_recommendations: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'success': False, 'error': 'Internal server error'})
        }
