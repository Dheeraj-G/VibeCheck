# Troubleshooting 404 NOT_FOUND Error

## Common Causes and Solutions

### 1. **Vercel Configuration Issues**

**Problem**: The `vercel.json` configuration might be incorrect.

**Solution**: Use the simplified configuration:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    },
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    },
    {
      "src": "api/**/*.js",
      "use": "@vercel/node"
    }
  ],
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9"
    }
  }
}
```

### 2. **Environment Variables Not Set**

**Problem**: Missing environment variables cause functions to fail.

**Check**: Go to Vercel Dashboard → Your Project → Settings → Environment Variables

**Required Variables**:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `GROQ_API_KEY`

### 3. **Python Dependencies Issues**

**Problem**: Python functions fail to load dependencies.

**Check**: Ensure `api/requirements.txt` exists and contains:
```
spotipy==2.23.0
requests==2.31.0
python-dotenv==1.0.0
groq
```

### 4. **File Path Issues**

**Problem**: Python code can't find `genres.json` file.

**Solution**: The code has been updated to use absolute paths.

### 5. **Function Structure Issues**

**Problem**: Vercel can't find the serverless functions.

**Check**: Ensure your API structure is:
```
api/
├── auth/
│   ├── login.js
│   ├── callback.js
│   └── refresh_token.js
├── recommendations/
│   ├── health.py
│   ├── track.py
│   ├── recommendations.py
│   └── prompt_recommendations.py
├── song_recommendations.py
├── genres.json
└── requirements.txt
```

## Debugging Steps

### Step 1: Check Vercel Function Logs
1. Go to Vercel Dashboard
2. Click on your project
3. Go to "Functions" tab
4. Check logs for any errors

### Step 2: Test Individual Endpoints
Try accessing these URLs directly:
- `https://your-project.vercel.app/api/recommendations/health`
- `https://your-project.vercel.app/api/auth/login`

### Step 3: Check Build Logs
1. Go to Vercel Dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Check the build logs for any errors

### Step 4: Verify Environment Variables
1. Go to Vercel Dashboard
2. Click on your project
3. Go to "Settings" → "Environment Variables"
4. Ensure all required variables are set

## Quick Fixes

### Fix 1: Redeploy with Updated Configuration
```bash
git add .
git commit -m "Fix Vercel configuration"
git push origin main
```

### Fix 2: Check Function Names
Ensure all Python files have the correct `handler` class:
```python
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Your code here
```

### Fix 3: Verify File Permissions
Ensure all files are committed to git and not ignored.

## Still Getting 404?

If you're still getting 404 errors:

1. **Check the exact URL** you're trying to access
2. **Verify the function exists** in the correct directory
3. **Check Vercel logs** for specific error messages
4. **Try redeploying** after making changes

## Contact Support

If none of these solutions work:
1. Check Vercel's documentation: https://vercel.com/docs
2. Check Vercel's GitHub issues: https://github.com/vercel/vercel
3. Contact Vercel support through their dashboard
