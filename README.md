# VibeCheck - Tempo-Based Music Discovery

VibeCheck is a music recommendation system that finds songs with the same tempo as your selected track, helping you discover music that matches your current vibe and energy level.

## Features

- **Spotify Integration**: Search and discover songs from Spotify's vast music library
- **Tempo Matching**: Find songs with the same tempo as your selected track
- **Real-time Search**: Autocomplete dropdown for Spotify song search
- **Clean Interface**: Simple, focused UI for tempo-based discovery

## Project Structure

```
VibeCheck/
├── frontend/                 # Next.js frontend application
│   ├── src/app/
│   │   ├── page.tsx         # Main application page
│   │   └── api/             # API routes
│   └── package.json
├── song_recommendations.py   # Core tempo-based recommendation engine
├── recommendations_server.py # Flask API server
├── requirements.txt          # Python dependencies
└── README.md
```

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Spotify Developer Account** with API credentials

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
PORT=5001
```

#### Run the Flask Server

```bash
python3 recommendations_server.py
```

The backend API will be available at `http://localhost:5001`

### 3. Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Get your `Client ID` and `Client Secret`
4. Add `http://localhost:3000/callback` to your redirect URIs
5. Update your `.env` file with these credentials

## API Endpoints

### Backend (Flask)

- `GET /health` - Health check
- `POST /recommendations` - Get tempo-based song recommendations
- `POST /track` - Get track information

### Frontend (Next.js)

- `POST /api/recommendations` - Frontend API route

## Usage

1. **Search for Songs**: Use the top search bar to find songs on Spotify
2. **Select a Song**: Click on a song to select it
3. **Get Tempo Matches**: The system will find 5 songs with the same tempo
4. **Explore**: Browse through the tempo-matched songs

## How It Works

1. **Song Selection**: User searches and selects a song from Spotify
2. **Tempo Extraction**: The system extracts the tempo (BPM) of the selected song
3. **Tempo Matching**: Uses Spotify's recommendation API to find songs with similar tempo
4. **Results Display**: Presents 5 songs with matching tempo and album artwork

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

### Testing

Test the Python engine:

```bash
python3 song_recommendations.py
```

Test the Flask server:

```bash
curl http://localhost:5001/health
```

## Troubleshooting

### Common Issues

1. **Spotify Authentication**: Check your environment variables and redirect URI
2. **CORS Issues**: The Flask server has CORS enabled, but check browser console for errors
3. **Port Conflicts**: Ensure ports 3000 (frontend) and 5001 (backend) are available

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

**Note**: This is a development version focused on tempo-based music discovery. For production use, ensure proper security measures, error handling, and rate limiting are implemented.
