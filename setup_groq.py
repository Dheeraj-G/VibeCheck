#!/usr/bin/env python3
"""
Groq API Setup Script for VibeCheck
Replaces local Ollama models with cloud-based Groq API
"""

import os
import sys
import requests
import json

def check_groq_api_key():
    """Check if Groq API key is set"""
    api_key = os.getenv('GROQ_API_KEY')
    if api_key and api_key != 'your_groq_api_key_here':
        print("✅ Groq API key found in environment")
        return True
    else:
        print("❌ Groq API key not found or not set")
        return False

def test_groq_connection():
    """Test connection to Groq API"""
    print("\n🔍 Testing Groq API connection...")
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key or api_key == 'your_groq_api_key_here':
        print("❌ No valid API key available for testing")
        return False
    
    # Test with a simple completion
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'llama3-8b-8192',
        'messages': [
            {
                'role': 'user',
                'content': 'Hello, this is a test message.'
            }
        ],
        'max_tokens': 50,
        'temperature': 0.1
    }
    
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Groq API connection successful!")
            return True
        else:
            print(f"❌ Groq API test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def setup_environment_file():
    """Create or update .env file with Groq configuration"""
    print("\n📝 Setting up environment configuration...")
    
    env_file = '.env'
    example_env = 'env.example'
    
    # If .env doesn't exist, copy from env.example
    if not os.path.exists(env_file):
        if os.path.exists(example_env):
            print("   Copying .env from env.example...")
            import shutil
            shutil.copy(example_env, env_file)
            print("   ✅ Created .env file from env.example")
        else:
            print("   Creating new .env file...")
            # Create basic .env file
            basic_config = [
                "# Spotify API Credentials\n",
                "# Get these from https://developer.spotify.com/dashboard\n",
                "SPOTIFY_CLIENT_ID=your_spotify_client_id_here\n",
                "SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here\n",
                "SPOTIFY_REDIRECT_URI=http://localhost:3000/callback\n",
                "\n# Flask Configuration\n",
                "FLASK_ENV=development\n",
                "PORT=5001\n",
                "\n# Groq API Configuration\n",
                "# Get your API key from https://console.groq.com/keys\n",
                "GROQ_API_KEY=your_groq_api_key_here\n",
                "GROQ_MODEL=llama3-8b-8192\n"
            ]
            with open(env_file, 'w') as f:
                f.writelines(basic_config)
            print("   ✅ Created new .env file")
    
    # Read existing .env file
    with open(env_file, 'r') as f:
        env_content = f.readlines()
    
    # Check if GROQ_API_KEY already exists
    groq_key_exists = any(line.startswith('GROQ_API_KEY=') for line in env_content)
    
    if not groq_key_exists:
        print("   Adding Groq API configuration to .env file...")
        
        # Add Groq configuration
        groq_config = [
            "\n# Groq API Configuration\n",
            "# Get your API key from: https://console.groq.com/keys\n",
            "GROQ_API_KEY=your_groq_api_key_here\n",
            "GROQ_MODEL=llama3-8b-8192\n"
        ]
        
        with open(env_file, 'a') as f:
            f.writelines(groq_config)
        
        print("   ✅ Added Groq configuration to .env file")
        print("   ⚠️  Please edit .env and add your actual Groq API key")
    else:
        print("   ✅ Groq API key already configured in .env file")
    
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing required dependencies...")
    
    try:
        import groq
        print("   ✅ groq package already installed")
    except ImportError:
        print("   Installing groq package...")
        os.system(f"{sys.executable} -m pip install groq")
        print("   ✅ groq package installed")
    
    # Check other required packages
    required_packages = ['requests', 'python-dotenv', 'spotipy']
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} already installed")
        except ImportError:
            print(f"   Installing {package}...")
            os.system(f"{sys.executable} -m pip install {package}")
            print(f"   ✅ {package} installed")
    
    return True

def verify_spotify_setup():
    """Check if Spotify credentials are configured"""
    print("\n🎵 Checking Spotify configuration...")
    
    spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
    spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if spotify_client_id and spotify_client_secret and spotify_client_id != 'your_spotify_client_id_here':
        print("   ✅ Spotify credentials found")
        return True
    else:
        print("   ⚠️  Spotify credentials not found")
        print("   Please add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to .env file")
        print("   Get them from: https://developer.spotify.com/dashboard")
        return False

def main():
    """Main setup function"""
    print("🎵 VibeCheck Groq API Setup")
    print("=" * 35)
    
    # Step 0: Load environment variables FIRST
    print("📖 Loading environment variables...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("   ✅ Environment variables loaded")
        
        # Debug: Show what was loaded
        groq_key = os.getenv('GROQ_API_KEY', 'NOT_FOUND')
        spotify_id = os.getenv('SPOTIFY_CLIENT_ID', 'NOT_FOUND')
        print(f"   📋 GROQ_API_KEY: {'***' + groq_key[-4:] if len(groq_key) > 8 and groq_key != 'NOT_FOUND' else groq_key}")
        print(f"   📋 SPOTIFY_CLIENT_ID: {'***' + spotify_id[-4:] if len(spotify_id) > 8 and spotify_id != 'NOT_FOUND' else spotify_id}")
        
    except ImportError:
        print("   ⚠️  python-dotenv not available, using system environment")
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        return False
    
    # Step 2: Setup environment file
    if not setup_environment_file():
        print("\n❌ Failed to setup environment file")
        return False
    
    # Step 3: Check Spotify setup
    verify_spotify_setup()
    
    # Step 4: Check Groq API key
    if not check_groq_api_key():
        print("\n📝 Please add your Groq API key to .env file:")
        print("1. Go to: https://console.groq.com/keys")
        print("2. Create a new API key")
        print("3. Add it to .env file: GROQ_API_KEY=your_key_here")
        print("4. Run this script again")
        return False
    
    # Step 5: Test Groq connection
    if not test_groq_connection():
        print("\n❌ Groq API connection failed")
        print("Please check your API key and internet connection")
        return False
    
    print("\n🎉 Groq API setup completed successfully!")
    print("You can now run the VibeCheck application.")
    print("\nNext steps:")
    print("1. Ensure your Spotify API credentials are in .env file")
    print("2. Run: python recommendations_server.py")
    print("3. In another terminal: cd frontend && npm run dev")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
