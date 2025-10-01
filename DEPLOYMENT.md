# VibeCheck - Vercel Deployment Guide

## Prerequisites

1. **Spotify Developer Account**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Note your Client ID and Client Secret

2. **Groq API Key**
   - Go to [Groq Console](https://console.groq.com/)
   - Create an account and get your API key

3. **Vercel Account**
   - Sign up at [Vercel](https://vercel.com)

## Step 1: Deploy to Vercel

1. **Connect Repository**
   - Go to your Vercel dashboard
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect the Next.js frontend

2. **Set Environment Variables**
   In your Vercel project settings, add these environment variables:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   GROQ_API_KEY=your_groq_api_key
   ```

## Step 2: Configure Spotify App

1. **Go to Spotify Developer Dashboard**
   - Navigate to your app settings
   - Click "Edit Settings"

2. **Add Redirect URIs**
   Add these redirect URIs (replace `your-project-name` with your actual Vercel project name):
   ```
   https://your-project-name.vercel.app/api/auth/callback
   ```

3. **Save Settings**
   - Click "Save" to apply the changes

## Step 3: Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Vercel"
   git push origin main
   ```

2. **Vercel Auto-Deploy**
   - Vercel will automatically detect the changes and deploy
   - Your app will be available at `https://your-project-name.vercel.app`

## Step 4: Test Deployment

1. **Visit your app**: `https://your-project-name.vercel.app`
2. **Test Authentication**:
   - Click "Login with Spotify"
   - Complete the OAuth flow
   - You should be redirected back to your app

3. **Test Recommendations**:
   - Enter a prompt like "upbeat summer road trip"
   - Click "Get Artists"
   - You should see AI-powered recommendations

## Troubleshooting

### Common Issues

1. **OAuth Redirect URI Mismatch**
   - Ensure the redirect URI in Spotify matches your Vercel domain exactly
   - Format: `https://your-project-name.vercel.app/api/auth/callback`

2. **Environment Variables Not Set**
   - Verify all environment variables are set in Vercel dashboard
   - Redeploy after adding new environment variables

3. **Python Dependencies**
   - Ensure `requirements.txt` is in the `/api` directory
   - Check Vercel function logs for Python errors

4. **CORS Issues**
   - The serverless functions include CORS headers
   - Check function responses in Vercel dashboard

### Checking Logs

1. Go to your Vercel project dashboard
2. Click on "Functions" tab
3. Check logs for any errors

### Testing API Endpoints

Test these endpoints after deployment:
- `GET https://your-project.vercel.app/api/recommendations/health`
- `POST https://your-project.vercel.app/api/recommendations/prompt_recommendations`

## Local Development (Optional)

If you want to test locally before deploying:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Run locally**:
   ```bash
   vercel dev
   ```

4. **Set local environment variables**:
   Create `.env.local` in the root directory:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   GROQ_API_KEY=your_groq_key
   ```

## Production Considerations

- **Rate Limits**: Be aware of Spotify API rate limits
- **Caching**: Consider implementing caching for recommendations
- **Error Handling**: Monitor function logs in Vercel dashboard
- **Security**: Never commit API keys to version control
- **Custom Domain**: You can add a custom domain in Vercel settings

## Support

If you encounter issues:
1. Check Vercel function logs
2. Verify Spotify app settings
3. Ensure all environment variables are set
4. Check the browser console for frontend errors