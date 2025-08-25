# VibeCheck - AI-Powered Music Discovery

VibeCheck is an intelligent music recommendation system that combines Spotify's music data with AI-powered natural language processing to help users discover new music based on their preferences and mood.

## Features

- **Spotify Integration**: Search and discover songs from Spotify's vast music library
- **AI-Powered Recommendations**: Use natural language to describe the vibe you're looking for
- **Smart Song Matching**: Combines selected song features with natural language prompts
- **Beautiful UI**: Modern, responsive interface with smooth animations
- **Real-time Search**: Autocomplete dropdown for Spotify song search

## Project Structure

```
VibeCheck/
├── frontend/                 # Next.js frontend application
│   ├── src/app/
│   │   ├── page.tsx         # Main application page
│   │   └── api/             # API routes
│   └── package.json
├── song_recommendations.py   # Core recommendation engine
├── recommendations_server.py # Flask API server
├── requirements.txt          # Python dependencies
└── README.md
```

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Spotify Developer Account** with API credentials
- **Groq API Key** for AI-powered recommendations

## Setup Instructions

### 1. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 2. Backend Setup

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Set up Environment Variables

Create a `.env` file in the root directory:

```bash
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/callback

# Flask Configuration
FLASK_ENV=development
PORT=5000

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
```

#### Set up Groq API

**Option 1: Automated Setup (Recommended)**
```bash
python setup_groq.py
```

**Option 2: Manual Setup**
1. Get your API key from [https://console.groq.com/keys](https://console.groq.com/keys)
2. Add it to your `.env` file:
   ```bash
   GROQ_API_KEY=your_actual_api_key_here
   ```

**Verify Setup**
```bash
python test_groq_simple.py
```

#### Run the Flask Server

```bash
python recommendations_server.py
```

The backend API will be available at `http://localhost:5000`

### 3. Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Get your `Client ID` and `Client Secret`
4. Add `http://localhost:3000/callback` to your redirect URIs
5. Update your `.env` file with these credentials

## API Endpoints

### Backend (Flask)

- `GET /health` - Health check with Ollama status
- `GET /search?q=<query>&limit=<limit>` - Search songs on Spotify
- `POST /recommendations` - Get song recommendations
- `GET /song-features/<song_id>` - Get audio features for a song
- `GET /similar-songs/<song_id>` - Get similar songs
- `GET /ollama/models` - Get available Ollama models
- `POST /ollama/download/<model_name>` - Download specific Ollama model

### Frontend (Next.js)

- `POST /api/recommendations` - Frontend API route (currently returns mock data)

## Usage

1. **Search for Songs**: Use the top search bar to find songs on Spotify
2. **Describe Your Vibe**: Use the natural language prompt to describe the music you want
3. **Get Recommendations**: Click "Get Recommendations" to receive AI-powered song suggestions
4. **Explore**: Browse through the recommended songs in the carousel

## How It Works

1. **Song Selection**: User searches and selects a song from Spotify
2. **Feature Extraction**: The system extracts audio features (tempo, energy, danceability, etc.)
3. **Natural Language Processing**: Ollama processes the user's natural language prompt
4. **Feature Blending**: Combines song features with prompt-derived features
5. **Recommendation Generation**: Uses Spotify's recommendation API to find similar songs
6. **Results Display**: Presents 5 recommended songs with album artwork

## Development

### Frontend Development

The frontend is built with:
- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **React 19** with modern hooks

### Backend Development

The backend uses:
- **Python 3.8+** for the core engine
- **Flask** for the web API
- **Spotipy** for Spotify API integration
- **Ollama** for AI-powered natural language processing

### Testing

Test the Python engine:

```bash
python song_recommendations.py
```

Test the Flask server:

```bash
curl http://localhost:5000/health
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**: 
   - Ensure Ollama is running (`ollama serve`)
   - Check if the model is downloaded (`ollama list`)
   - Run the setup script: `python setup_ollama.py`

2. **Llama 3 Model Issues**:
   - Download the model: `ollama pull llama3.1:8b`
   - Check model status: `curl http://localhost:5000/ollama/models`
   - Download via API: `POST http://localhost:5000/ollama/download/llama3.1:8b`

3. **Spotify Authentication**: Check your environment variables and redirect URI
4. **CORS Issues**: The Flask server has CORS enabled, but check browser console for errors
5. **Port Conflicts**: Ensure ports 3000 (frontend) and 5000 (backend) are available

### Debug Mode

Enable debug mode for the Flask server by setting `FLASK_ENV=development` in your `.env` file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub

---

**Note**: This is a development version. For production use, ensure proper security measures, error handling, and rate limiting are implemented.
