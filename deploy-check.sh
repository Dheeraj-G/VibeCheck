#!/bin/bash

echo "🚀 VibeCheck Deployment Helper"
echo "================================"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if vercel.json exists
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found!"
    exit 1
fi

# Check if environment variables are documented
echo "📋 Pre-deployment checklist:"
echo ""

# Check for required files
echo "✅ Required files:"
[ -f "vercel.json" ] && echo "   ✓ vercel.json"
[ -f "api/requirements.txt" ] && echo "   ✓ api/requirements.txt"
[ -f "frontend/package.json" ] && echo "   ✓ frontend/package.json"
[ -f "api/song_recommendations.py" ] && echo "   ✓ api/song_recommendations.py"
[ -f "api/genres.json" ] && echo "   ✓ api/genres.json"

echo ""
echo "🔧 Environment Variables needed in Vercel:"
echo "   • SPOTIFY_CLIENT_ID"
echo "   • SPOTIFY_CLIENT_SECRET" 
echo "   • GROQ_API_KEY"

echo ""
echo "🎵 Spotify App Configuration:"
echo "   • Redirect URI: https://your-project-name.vercel.app/api/auth/callback"
echo "   • Scopes: user-read-private user-read-email user-library-read playlist-read-private app-remote-control"

echo ""
echo "📝 Next steps:"
echo "   1. Push to GitHub: git push origin main"
echo "   2. Connect repository to Vercel"
echo "   3. Set environment variables in Vercel dashboard"
echo "   4. Update Spotify app redirect URI"
echo "   5. Deploy!"

echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
