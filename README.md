# VibeCheck - Music Recommendation App

A modern music recommendation app built with Next.js, Python, and Spotify API, deployed as a monorepo on Vercel.

## Features

- **Spotify OAuth Authentication**: Secure login with Spotify
- **AI-Powered Recommendations**: Uses Groq AI to understand natural language prompts and suggest artists
- **Song-Based Recommendations**: Get recommendations based on specific songs
- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **Serverless Architecture**: Deployed on Vercel with serverless functions

## Architecture

This is a monorepo containing:

- **Frontend**: Next.js app in `/frontend`
- **API**: Serverless functions in `/api`
  - **Auth**: OAuth endpoints (`/api/auth/`)
  - **Recommendations**: Python-based recommendation engine (`/api/recommendations/`)

## Environment Variables

Set these environment variables in your Vercel dashboard:

- `SPOTIFY_CLIENT_ID`: Your Spotify app client ID
- `SPOTIFY_CLIENT_SECRET`: Your Spotify app client secret
- `GROQ_API_KEY`: Your Groq API key

## Local Development

1. Install dependencies:
   ```bash
   npm install
   cd frontend && npm install
   ```

2. Set up environment variables:
   Create a `.env.local` file in the root directory:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   GROQ_API_KEY=your_groq_api_key
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Quick Deployment

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to Vercel"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

3. **Set Environment Variables** in Vercel dashboard:
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
   - `GROQ_API_KEY`

4. **Configure Spotify App**:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Add redirect URI: `https://your-project-name.vercel.app/api/auth/callback`

5. **Deploy!** Vercel will automatically build and deploy your app.

For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

## API Endpoints

### Authentication
- `GET /api/auth/login` - Initiate Spotify OAuth flow
- `GET /api/auth/callback` - Handle OAuth callback
- `GET /api/auth/refresh_token` - Refresh access token

### Recommendations
- `GET /api/recommendations/health` - Health check
- `POST /api/recommendations/track` - Get track information
- `POST /api/recommendations/recommendations` - Get song-based recommendations
- `POST /api/recommendations/prompt_recommendations` - Get AI-powered recommendations

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Python, Flask (converted to serverless)
- **Authentication**: Spotify OAuth 2.0
- **AI**: Groq API for natural language processing
- **Deployment**: Vercel
- **Music Data**: Spotify Web API

## License

MIT