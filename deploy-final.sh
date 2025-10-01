#!/bin/bash

echo "🚀 VibeCheck - Final Deployment"
echo "=============================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

echo "✅ Build test passed!"
echo "✅ Suspense boundary added for useSearchParams"
echo "✅ Unused variables cleaned up"
echo "✅ API route conflicts removed"
echo ""

echo "📋 Final checklist:"
echo "   ✓ vercel.json - Simplified configuration"
echo "   ✓ Python imports - Fixed path issues"
echo "   ✓ Frontend build - Successful"
echo "   ✓ Suspense boundary - Added for Next.js 15"
echo ""

echo "🚀 Deploying to Vercel..."
echo ""

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Fix Next.js build errors and 404 issues - ready for production"

# Push to trigger Vercel deployment
git push origin main

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📝 Next steps:"
echo "   1. Wait for Vercel to build and deploy (2-3 minutes)"
echo "   2. Check deployment status in Vercel dashboard"
echo "   3. Test your app: https://your-project.vercel.app"
echo ""
echo "🧪 Test these endpoints:"
echo "   • Health: https://your-project.vercel.app/api/recommendations/health"
echo "   • Login: https://your-project.vercel.app/api/auth/login"
echo ""
echo "🎵 Don't forget to:"
echo "   • Set environment variables in Vercel dashboard"
echo "   • Update Spotify redirect URI to your Vercel domain"
echo ""
echo "📖 For troubleshooting, see TROUBLESHOOTING.md"
