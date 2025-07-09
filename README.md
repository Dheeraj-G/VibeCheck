# Vibe Check 🎧

**Vibe Check** is a mobile app designed to help you discover songs that match the *vibe* of whatever you're feeling right now.

## 🎯 Goal
Find songs based on the current vibe of a track you love — no more endless searching. Just pick a song, and let Vibe Check do the rest.

## 🔍 How It Works
- Start by choosing a song.
- The app analyzes key metrics using the Spotify API:
  - **Genre**
  - **Tempo**
  - **Danceability**
  - And other audio features
- It then adds 10 vibe-matched songs to your queue.

## ❤️ Preference Learning
- Users can **like** or **dislike** suggestions.
- A lightweight model learns your taste over time to improve future recommendations.
- Each new "vibe session" (when you pick a new base song) resets preferences to stay true to your new mood.

## 🛠 Tech Stack

### 🎨 Design
- Designed in **Figma** for a clean, intuitive interface.

### 🧩 Frontend
- Built using Next JS
- Optionally: Used as a **Spotify extension** instead of a standalone interface.

### 🧠 Backend
- Powered by **Python**.
- Integrated with:
  - **Spotify API** for song and audio feature data.
  - An **AI model API** to refine recommendations.

---

Stay tuned for a smoother, smarter, and more *vibe-aware* music experience.
