import logging
import os
from typing import Dict, List, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv
import requests
import json
from groq import Groq

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SongRecommendationsEngine:

    def __init__(self):
        self.spotify_client = self._init_spotify_client()
        self.song_cache = {}
        self.groq_client = self._init_groq_client()
        self.test_spotify_connection()
    
        try:
            with open("genres.json", "r") as f:
                genres = json.load(f)
            self.allowed_genres = set(map(str.lower, genres))  # normalize to lowercase
            logger.info(f"Loaded {len(self.allowed_genres)} Spotify genres.")
        except Exception as e:
            logger.error(f"Failed to load genres: {e}")
            self.allowed_genres = set()

    def test_spotify_connection(self):
        try:
            # Simple test - get a popular track
            results = self.spotify_client.track('4iV5W9uYEdYUVa79Axb7Rh')  # Hotel California
            logging.info(f"Test successful: {results['name']}")
            return True
        except Exception as e:
            logging.error(f"Connection test failed: {e}")
            return False

    def _init_spotify_client(self):
        try:
            # Get credentials from environment variables
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

            if not client_id or not client_secret:
                logger.warning("Spotify credentials not found in environment variables.")
                return None

            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            sp = spotipy.Spotify(auth_manager=auth_manager)
            logger.info("Spotify client initialized successfully.")
            return sp
        except Exception as e:
            logger.error(f"Error initializing Spotify client: {e}")
            return None

    def _get_spotify_client(self, user_token: str = None):
        """Create a Spotify client with user token for higher API access"""
        if not user_token:
            logger.info("No user token provided, using client credentials")
            return self.spotify_client

        try:
            # When using a user's access token, pass it directly as auth parameter
            sp = spotipy.Spotify(auth=user_token)
            # Test the token by making a simple API call
            sp.current_user()
            logger.info("Successfully created Spotify client with user token")
            return sp
        except Exception as e:
            logger.warning(f"Failed to create user Spotify client: {e}. Falling back to client credentials.")
            return self.spotify_client

    def _init_groq_client(self) -> Optional[Groq]:
        try:
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                logger.warning("GROQ_API_KEY not set; Groq features disabled.")
                return None
            client = Groq(api_key=api_key)
            logger.info("Groq client initialized successfully.")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            return None

    def _normalize_genre(self, text: str) -> Optional[str]:
        if not text:
            return None
        text_lower = text.strip().lower()
        text_lower = text_lower.capitalize()
        
        return text_lower.split(',')[0].split('\n')[0].strip(' .') or None

    def _genre_from_prompt_via_groq(
    self,
    prompt: str,
    allowed_genres: Optional[set] = None
) -> Optional[str]:
        """Query Groq for a genre using only the allowed genres."""

        if not self.groq_client:
            return None

        if allowed_genres is None:
            allowed_genres = self.allowed_genres or set()

        if not allowed_genres:
            logger.warning("No allowed genres provided.")
            return None

        try:
            model = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')

            full_prompt = f"""
            You are a music genre selector. Your job is to imagine what the user prompt would be like a choose the best fitting genre.
            Return exactly one genre from this list and do not invent new genres: {sorted(list(allowed_genres))}.
            Return only the genre name from the list. If unsure, respond with "none".
            No extra words, no explanations. Example: "rock", not "Rock music".

            User said: "{prompt}"

            Respond with exactly one genre name from the list only.
            """

            completion = self.groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.2,
                max_tokens=8,
                top_p=1,
                stream=False,
            )

            content = completion.choices[0].message.content.strip().lower()
            normalized = self._normalize_genre(content)
            return normalized

        except Exception as e:
            logger.warning(f"Groq genre extraction failed: {e}")
            return None

    def find_artists_by_genre(self, genre: str, user_token: str = None, limit: int = 6) -> List[Dict]:
        spotify_client = self._get_spotify_client(user_token)
        if not spotify_client:
            logger.error("No Spotify client available")
            return []
        try:
            query = f'genre:"{genre}"'
            search_res = spotify_client.search(q=query, type='artist', limit=50)
            artist_items = (search_res.get('artists') or {}).get('items', [])
            results = []
            for a in artist_items:
                if not a:
                    continue
                popularity = a.get('popularity', 0)
                images = a.get('images') or []
                image_url = images[0]['url'] if images else None
                results.append({
                    "id": a.get('id'),
                    "name": a.get('name'),
                    "artist": genre,
                    "album": "",
                    "imageUrl": image_url,
                    "popularity": popularity
                })
                if len(results) >= limit:
                    break
            return results
        except SpotifyException as e:
            logger.error(f"Spotify API error finding artists by genre: {e.http_status} - {e.msg}")
            if e.http_status == 401 and user_token and spotify_client != self.spotify_client:
                logger.info("Retrying with client credentials...")
                return self.find_artists_by_genre(genre, user_token=None, limit=limit)
            return []
        except Exception as e:
            logger.error(f"Unexpected error finding artists by genre: {type(e).__name__} - {e}")
            return []

    def get_song_tempo(self, song_id: str, user_token: str = None) -> Optional[float]:
        """Get the tempo of a song"""
        # Check cache first
        if song_id in self.song_cache:
            cached_tempo = self.song_cache[song_id].get('tempo')
            logger.info(f"Returning cached tempo for {song_id}: {cached_tempo} BPM")
            return cached_tempo

        # Try user token first, then fall back to client credentials
        spotify_client = self._get_spotify_client(user_token)
        
        if not spotify_client:
            logger.error("No Spotify client available")
            return None

        try:
            # First verify the track exists
            logger.info(f"Fetching track info for {song_id}")
            track = spotify_client.track(song_id)
            logger.info(f"Track found: {track['name']} by {track['artists'][0]['name']}")
            
            # Then get audio features
            logger.info(f"Fetching audio features for {song_id}")
            features = spotify_client.audio_features([song_id])
            
            if not features or not features[0]:
                logger.error(f"No audio features returned for {song_id}")
                # If using user token and it failed, try with client credentials
                if user_token and spotify_client != self.spotify_client:
                    logger.info("Retrying with client credentials...")
                    return self.get_song_tempo(song_id, user_token=None)
                return None
                
            feature_data = features[0]
            
            if not feature_data:
                logger.error(f"Audio features data is None for {song_id}")
                if user_token and spotify_client != self.spotify_client:
                    logger.info("Retrying with client credentials...")
                    return self.get_song_tempo(song_id, user_token=None)
                return None
            
            tempo = feature_data.get('tempo')
            
            if tempo is None:
                logger.error(f"Tempo field is None in audio features for {song_id}")
                logger.error(f"Available features: {list(feature_data.keys())}")
                return None
            
            # Cache the tempo
            self.song_cache[song_id] = {'tempo': tempo}
            logger.info(f"Successfully fetched tempo for {song_id}: {tempo} BPM")
            return tempo
            
        except SpotifyException as e:
            logger.error(f"Spotify API error for {song_id}: {e.http_status} - {e.msg}")
            # If unauthorized and using user token, retry with client credentials
            if e.http_status == 401 and user_token and spotify_client != self.spotify_client:
                logger.info("Token unauthorized, retrying with client credentials...")
                return self.get_song_tempo(song_id, user_token=None)
            elif e.http_status == 404:
                logger.error(f"Track {song_id} not found. Check if the ID is valid.")
            elif e.http_status == 429:
                logger.error(f"Rate limit exceeded. Wait before retrying.")
            return None
        except IndexError as e:
            logger.error(f"Index error fetching features for {song_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching tempo for {song_id}: {type(e).__name__} - {e}")
            # Last resort: try with client credentials if we were using user token
            if user_token and spotify_client != self.spotify_client:
                logger.info("Unexpected error, retrying with client credentials...")
                return self.get_song_tempo(song_id, user_token=None)
            return None

    def find_songs_by_tempo(self, target_tempo: float, user_token: str = None) -> List[Dict]:
        """Find songs with similar tempo using Spotify's search and recommendations"""
        spotify_client = self._get_spotify_client(user_token)
        
        if not spotify_client:
            logger.error("No Spotify client available")
            return []

        try:
            # Use Spotify's recommendations API with tempo target
            logger.info(f"Fetching recommendations for tempo: {target_tempo} BPM")
            recs = spotify_client.recommendations(
                seed_tracks=['4iV5W9uYEdYUVa79Axb7Rh'],  # Hotel California as seed
                limit=20,  # Get more to filter by tempo
                target_tempo=target_tempo,
                min_tempo=max(0, target_tempo - 10),
                max_tempo=target_tempo + 10
            )
            
            recommendations = []
            for track in recs.get("tracks", []):
                recommendations.append({
                    "id": track["id"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "imageUrl": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                })
            
            # Return first 5 songs
            result = recommendations[:5]
            logger.info(f"Found {len(result)} songs with tempo around {target_tempo} BPM")
            return result
            
        except SpotifyException as e:
            logger.error(f"Spotify API error finding songs by tempo: {e.http_status} - {e.msg}")
            # Retry with client credentials if user token failed
            if e.http_status == 401 and user_token and spotify_client != self.spotify_client:
                logger.info("Retrying with client credentials...")
                return self.find_songs_by_tempo(target_tempo, user_token=None)
            return []
        except Exception as e:
            logger.error(f"Unexpected error finding songs by tempo: {type(e).__name__} - {e}")
            return []

    def get_track_info(self, track_id: str) -> Optional[Dict]:
        """Get basic track information"""
        if not self.spotify_client:
            return None
            
        try:
            track = self.spotify_client.track(track_id)
            return {
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "imageUrl": track["album"]["images"][0]["url"] if track["album"]["images"] else None
            }
        except SpotifyException as e:
            logger.error(f"Spotify API error fetching track {track_id}: {e.http_status} - {e.msg}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching track info for {track_id}: {type(e).__name__} - {e}")
            return None

    def get_recommendations(self, selected_song_id: str = None, user_token: str = None) -> Dict:
        if not selected_song_id:
            return {"success": False, "error": "No song ID provided", "seed_song_id": None}

        logger.info(f"Getting artist-based recommendations for song: {selected_song_id}")

        spotify_client = self._get_spotify_client(user_token)
        if not spotify_client:
            error_msg = "No Spotify client available"
            logger.error(error_msg)
            return {"success": False, "error": error_msg, "seed_song_id": selected_song_id}

        try:
            # 1) Get the track and its primary artist
            track = spotify_client.track(selected_song_id)
            if not track or not track.get('artists'):
                error_msg = f"Track not found or has no artists: {selected_song_id}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg, "seed_song_id": selected_song_id}

            primary_artist = track['artists'][0]
            primary_artist_id = primary_artist['id']

            # 2) Fetch the artist details to get genres and popularity
            artist_obj = spotify_client.artist(primary_artist_id)
            artist_genres = artist_obj.get('genres', [])
            artist_popularity = artist_obj.get('popularity')
            logger.info(f"Seed artist: {artist_obj.get('name')} (pop {artist_popularity}), genres: {artist_genres}")

            if not artist_genres:
                error_msg = f"Seed artist has no genres: {artist_obj.get('name')}"
                logger.warning(error_msg)
                return {"success": False, "error": error_msg, "seed_song_id": selected_song_id}

            top_genre = artist_genres[0]

            # 3) Search for artists by the top genre
            # Use Spotify search with genre filter
            query = f'genre:"{top_genre}"'
            search_res = spotify_client.search(q=query, type='artist', limit=50)
            artist_items = (search_res.get('artists') or {}).get('items', [])

            # 4) Filter artists by popularity between 25 and 75 (inclusive) and exclude the seed artist
            filtered = []
            for a in artist_items:
                if not a:
                    continue
                if a.get('id') == primary_artist_id:
                    continue
                popularity = a.get('popularity', 0)
                if 25 <= popularity <= 75:
                    images = a.get('images') or []
                    image_url = images[0]['url'] if images else None
                    # Reuse the existing front-end shape: name, artist, album, imageUrl
                    # - name: artist name
                    # - artist: top genre string
                    # - album: empty for artists
                    filtered.append({
                        "id": a.get('id'),
                        "name": a.get('name'),
                        "artist": top_genre,
                        "album": "",
                        "imageUrl": image_url,
                        "popularity": popularity
                    })

            # 5) Take the first 5
            recommendations = filtered[:5]

            if not recommendations:
                error_msg = f"No artists found in genre '{top_genre}' within popularity 25-75"
                logger.warning(error_msg)
                return {"success": False, "error": error_msg, "seed_song_id": selected_song_id, "genre": top_genre}

            logger.info(f"Found {len(recommendations)} artist recommendations in genre '{top_genre}'")
            return {
                "success": True,
                "songs": recommendations,
                "seed_song_id": selected_song_id,
                "genre": top_genre,
                "artist_based": True
            }

        except SpotifyException as e:
            logger.error(f"Spotify API error in artist-based recommendations: {e.http_status} - {e.msg}")
            # Retry with client credentials if user token failed
            if e.http_status == 401 and user_token and spotify_client != self.spotify_client:
                logger.info("Retrying with client credentials for artist-based recommendations...")
                return self.get_recommendations(selected_song_id, user_token=None)
            return {"success": False, "error": f"Spotify error: {e.msg}", "seed_song_id": selected_song_id}
        except Exception as e:
            logger.error(f"Unexpected error in artist-based recommendations: {type(e).__name__} - {e}")
            return {"success": False, "error": "Internal error creating recommendations", "seed_song_id": selected_song_id}