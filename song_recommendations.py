#!/usr/bin/env python3
"""
Song Recommendations Engine for VibeCheck
Handles Spotify API integration and Groq API-based natural language processing
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import groq

class SongRecommendationsEngine:
    def __init__(self):
        # Initialize Spotify client
        self.spotify_client = self._init_spotify_client()
        
        # Initialize Groq client
        self.groq_client = self._init_groq_client()
        
        # Cache for storing song features
        self.song_cache = {}
        
        # Verify Groq API setup
        self._verify_groq_setup()
        
    def _init_groq_client(self):
        """Initialize Groq API client"""
        try:
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                print("❌ GROQ_API_KEY not found in environment variables")
                return None
            
            # Use groq package if available, otherwise use requests
            try:
                client = groq.Groq(api_key=api_key)
                print("✅ Using groq package client")
                return client
            except ImportError:
                print("⚠️  groq package not available, using requests fallback")
                return None
                
        except Exception as e:
            print(f"❌ Error initializing Groq client: {e}")
            return None
        
    def _verify_groq_setup(self):
        """Verify Groq API is accessible"""
        try:
            if not self.groq_client:
                print("❌ Groq client not available")
                return False
            
            # Test with a simple completion
            test_response = self._call_groq_api(
                "Hello, this is a test message.",
                max_tokens=10
            )
            
            if test_response:
                print("✅ Groq API connection verified!")
                return True
            else:
                print("❌ Groq API test failed")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying Groq setup: {e}")
            return False
    
    def _call_groq_api(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7):
        """Call Groq API with fallback to requests"""
        try:
            api_key = os.getenv('GROQ_API_KEY')
            model = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
            
            if not api_key:
                print("❌ GROQ_API_KEY not found")
                return None
            
            # Try using groq package first
            if self.groq_client:
                try:
                    response = self.groq_client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    print(f"⚠️  groq package failed, falling back to requests: {e}")
            
            # Fallback to direct API calls
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': max_tokens,
                'temperature': temperature
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ Groq API error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error calling Groq API: {e}")
            return None
    
    def _init_spotify_client(self):
        """Initialize Spotify client with authentication"""
        try:
            # Try to use user authentication first (for user-specific features)
            scope = "user-read-private user-read-email playlist-read-private playlist-read-collaborative"
            auth_manager = SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                scope=scope
            )
            return spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            print(f"User authentication failed, falling back to client credentials: {e}")
            # Fallback to client credentials (limited access)
            auth_manager = SpotifyClientCredentials(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
            )
            return spotipy.Spotify(auth_manager=auth_manager)
    
    def search_songs(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for songs on Spotify"""
        try:
            results = self.spotify_client.search(
                q=query,
                type='track',
                limit=limit,
                market='US'
            )
            
            songs = []
            for track in results['tracks']['items']:
                song = {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'popularity': track['popularity'],
                    'duration_ms': track['duration_ms'],
                    'external_url': track['external_urls']['spotify']
                }
                songs.append(song)
            
            return songs
        except Exception as e:
            print(f"Error searching songs: {e}")
            return []
    
    def get_song_features(self, song_id: str) -> Optional[Dict[str, Any]]:
        """Get audio features for a specific song"""
        if song_id in self.song_cache:
            return self.song_cache[song_id]
        
        try:
            features = self.spotify_client.audio_features(song_id)[0]
            if features:
                # Cache the features
                self.song_cache[song_id] = features
                return features
        except Exception as e:
            print(f"Error getting song features: {e}")
        
        return None
    
    def get_similar_songs_by_features(self, song_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get similar songs based on audio features"""
        try:
            # Get recommendations based on seed track
            recommendations = self.spotify_client.recommendations(
                seed_tracks=[song_id],
                limit=limit,
                market='US'
            )
            
            similar_songs = []
            for track in recommendations['tracks']:
                song = {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'popularity': track['popularity'],
                    'external_url': track['external_urls']['spotify']
                }
                similar_songs.append(song)
            
            return similar_songs
        except Exception as e:
            print(f"Error getting similar songs: {e}")
            return []
    
    def get_similar_songs_by_metrics(self, target_features: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Get similar songs based on specific audio metrics"""
        try:
            # Create a seed track with similar features
            # This is a simplified approach - in production you'd want more sophisticated matching
            
            # Search for songs with similar characteristics
            # For now, we'll use the recommendation API with genre/artist seeds
            recommendations = self.spotify_client.recommendations(
                seed_genres=['pop'],  # Default genre, could be made dynamic
                limit=limit,
                market='US',
                target_energy=target_features.get('energy', 0.5),
                target_danceability=target_features.get('danceability', 0.5),
                target_valence=target_features.get('valence', 0.5),
                target_tempo=target_features.get('tempo', 120)
            )
            
            similar_songs = []
            for track in recommendations['tracks']:
                song = {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'popularity': track['popularity'],
                    'external_url': track['external_urls']['spotify']
                }
                similar_songs.append(song)
            
            return similar_songs
        except Exception as e:
            print(f"Error getting similar songs by metrics: {e}")
            return []
    
    def process_natural_language_prompt(self, prompt: str) -> Dict[str, Any]:
        """Process natural language prompt using Groq to extract musical preferences"""
        try:
            # Create a system prompt for the AI model
            system_prompt = """You are a music analysis expert. Given a natural language description of a musical vibe or preference, 
            extract the key musical characteristics and return them as a JSON object with the following structure:
            {
                "energy": float (0.0-1.0),
                "danceability": float (0.0-1.0), 
                "valence": float (0.0-1.0),
                "tempo": float (BPM),
                "acousticness": float (0.0-1.0),
                "instrumentalness": float (0.0-1.0),
                "liveness": float (0.0-1.0),
                "speechiness": float (0.0-1.0),
                "key": int (0-11),
                "mode": int (0=major, 1=minor),
                "time_signature": int (3-7),
                "description": "string explaining the vibe"
            }
            
            Only return valid JSON, no additional text."""
            
            # Check if we have a valid Groq client
            if not self.groq_client:
                print("❌ Groq client not available, using fallback features")
                return self._get_default_features(prompt)
            
            # Use Groq to process the prompt
            response = self._call_groq_api(
                system_prompt + "\n\n" + prompt,
                max_tokens=500
            )
            
            # Extract JSON from response
            content = response
            try:
                # Try to parse the JSON response
                parsed_features = json.loads(content)
                return parsed_features
            except json.JSONDecodeError:
                # If JSON parsing fails, return default features
                print(f"Failed to parse JSON from Groq response: {content}")
                return self._get_default_features(prompt)
                
        except Exception as e:
            print(f"Error processing natural language prompt: {e}")
            return self._get_default_features(prompt)
    
    def _get_default_features(self, prompt: str) -> Dict[str, Any]:
        """Get default features when Groq processing fails"""
        # Simple keyword-based fallback
        prompt_lower = prompt.lower()
        
        if 'energetic' in prompt_lower or 'upbeat' in prompt_lower:
            return {'energy': 0.8, 'danceability': 0.7, 'valence': 0.8, 'tempo': 140}
        elif 'chill' in prompt_lower or 'relaxed' in prompt_lower:
            return {'energy': 0.3, 'danceability': 0.4, 'valence': 0.6, 'tempo': 90}
        elif 'sad' in prompt_lower or 'melancholic' in prompt_lower:
            return {'energy': 0.4, 'danceability': 0.3, 'valence': 0.2, 'tempo': 80}
        elif 'happy' in prompt_lower or 'joyful' in prompt_lower:
            return {'energy': 0.7, 'danceability': 0.8, 'valence': 0.9, 'tempo': 120}
        else:
            return {'energy': 0.5, 'danceability': 0.5, 'valence': 0.5, 'tempo': 120}
    
    def get_recommendations(self, prompt: str, selected_song_id: Optional[str] = None) -> Dict[str, Any]:
        """Main method to get song recommendations"""
        try:
            # Process the natural language prompt
            extracted_features = self.process_natural_language_prompt(prompt)
            
            # If a song is selected, get its features and combine with prompt features
            if selected_song_id:
                song_features = self.get_song_features(selected_song_id)
                if song_features:
                    # Blend the features (50% from selected song, 50% from prompt)
                    blended_features = {}
                    for key in extracted_features:
                        if key in song_features and isinstance(song_features[key], (int, float)):
                            blended_features[key] = (song_features[key] + extracted_features[key]) / 2
                        else:
                            blended_features[key] = extracted_features[key]
                    
                    # Get recommendations based on blended features
                    recommended_songs = self.get_similar_songs_by_metrics(blended_features, limit=5)
                else:
                    # Fallback to prompt-only features
                    recommended_songs = self.get_similar_songs_by_metrics(extracted_features, limit=5)
            else:
                # Use only prompt features
                recommended_songs = self.get_similar_songs_by_metrics(extracted_features, limit=5)
            
            return {
                'success': True,
                'songs': recommended_songs,
                'extracted_features': extracted_features,
                'prompt': prompt
            }
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return {
                'success': False,
                'error': str(e),
                'songs': []
            }

# Example usage and testing
if __name__ == "__main__":
    # Set up environment variables (in production, use proper config management)
    os.environ.setdefault('SPOTIFY_CLIENT_ID', 'your_client_id_here')
    os.environ.setdefault('SPOTIFY_CLIENT_SECRET', 'your_client_secret_here')
    os.environ.setdefault('SPOTIFY_REDIRECT_URI', 'http://localhost:3000/callback')
    os.environ.setdefault('GROQ_API_KEY', 'your_groq_api_key_here') # Add GROQ_API_KEY
    os.environ.setdefault('GROQ_MODEL', 'llama3-8b-8192') # Add GROQ_MODEL
    
    # Initialize the engine
    engine = SongRecommendationsEngine()
    
    # Test the system
    print("Testing Song Recommendations Engine...")
    
    # Test 1: Search for songs
    print("\n1. Searching for 'Bohemian Rhapsody'...")
    songs = engine.search_songs("Bohemian Rhapsody", limit=3)
    for song in songs:
        print(f"  - {song['name']} by {song['artist']}")
    
    # Test 2: Process natural language prompt
    print("\n2. Processing prompt: 'I want energetic, upbeat music for working out'...")
    features = engine.process_natural_language_prompt("I want energetic, upbeat music for working out")
    print(f"  Extracted features: {json.dumps(features, indent=2)}")
    
    # Test 3: Get recommendations
    print("\n3. Getting recommendations...")
    if songs:
        recommendations = engine.get_recommendations(
            "I want energetic, upbeat music for working out",
            songs[0]['id']
        )
        print(f"  Success: {recommendations['success']}")
        if recommendations['success']:
            print("  Recommended songs:")
            for song in recommendations['songs']:
                print(f"    - {song['name']} by {song['artist']}")
    
    print("\nTesting complete!")
