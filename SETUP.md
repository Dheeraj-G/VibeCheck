# VibeCheck Setup Guide

## 🎵 **Groq API + Spotify Integration**

This application uses **Groq API** for AI-powered song recommendations and **Spotify API** for music data.

## 🚀 **Quick Setup**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Get API Keys**

#### **Groq API Key**
- Go to [https://console.groq.com/keys](https://console.groq.com/keys)
- Sign up/login and create a new API key
- Copy the key (starts with `gsk_`)

#### **Spotify API Keys**
- Go to [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
- Create a new app or use existing one
- Get your Client ID and Client Secret

### **3. Configure Environment**
```bash
# Copy the example file
cp env.example .env

# Edit .env with your actual API keys
SPOTIFY_CLIENT_ID=your_actual_client_id
SPOTIFY_CLIENT_SECRET=your_actual_client_secret
GROQ_API_KEY=your_actual_groq_api_key
```

### **4. Run Setup Script**
```bash
python3 setup_groq.py
```

### **5. Test Integration**
```bash
python3 test_groq_simple.py
```

### **6. Start the Application**
```bash
# Terminal 1: Backend
python3 recommendations_server.py

# Terminal 2: Frontend
cd frontend && npm install && npm run dev
```

## 🔧 **What Each File Does**

- **`setup_groq.py`** - Sets up Groq API and Spotify integration
- **`song_recommendations.py`** - Core recommendation engine using Groq API
- **`recommendations_server.py`** - Flask backend API server
- **`frontend/`** - Next.js web application
- **`test_groq_simple.py`** - Test script for Groq integration

## 🌟 **Benefits of Groq API**

- **No local resources** - Won't crash your computer
- **Fast inference** - Optimized for speed
- **Always available** - No need to manage local services
- **Free tier** - Generous free usage limits
- **Latest models** - Access to cutting-edge AI models

## 🚨 **Troubleshooting**

- **API key errors**: Ensure your `.env` file has the correct API keys
- **Spotify errors**: Check your Spotify app settings and redirect URI
- **Groq errors**: Verify your API key and internet connection

## 📱 **Access Your App**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
