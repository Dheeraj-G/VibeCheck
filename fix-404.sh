#!/bin/bash

echo "🔧 VibeCheck - Fixing 404 Error and Redeploying"
echo "=============================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

echo "📋 Changes made to fix 404 error:"
echo "   ✓ Simplified vercel.json configuration"
echo "   ✓ Fixed Python import paths"
echo "   ✓ Fixed genres.json file path loading"
echo "   ✓ Added better error handling"
echo ""

echo "🚀 Deploying fixes..."
echo ""

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Fix 404 NOT_FOUND error - simplify Vercel config and fix Python imports"

# Push to trigger Vercel deployment
git push origin main

echo ""
echo "✅ Changes pushed to GitHub!"
echo ""
echo "📝 Next steps:"
echo "   1. Wait for Vercel to automatically deploy"
echo "   2. Check Vercel dashboard for deployment status"
echo "   3. Test the health endpoint: https://your-project.vercel.app/api/recommendations/health"
echo "   4. Test the login: https://your-project.vercel.app/api/auth/login"
echo ""
echo "🔍 If still getting 404 errors:"
echo "   • Check Vercel function logs in dashboard"
echo "   • Verify environment variables are set"
echo "   • See TROUBLESHOOTING.md for more help"
echo ""
echo "📖 For detailed troubleshooting, see TROUBLESHOOTING.md"
