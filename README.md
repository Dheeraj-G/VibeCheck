# VibeCheck - Music Recommendation App 

A modern music recommendation app built with Next.js, Python, and Spotify API, deployed as a monorepo on Vercel.

## Visit
[VibeCheck](https://vibe-check-steel.vercel.app)

## Features

- **Spotify OAuth Authentication**: Secure login with Spotify
- **AI-Powered Recommendations**: Uses Groq AI to understand natural language prompts and suggest artists
- **Song-Based Recommendations**: Get recommendations based on your mood and the picture you paint
- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **Serverless Architecture**: Deployed on Vercel with serverless functions

## Architecture

This is a monorepo containing:

- **Frontend**: Next.js app in `/frontend`
- **API**: Serverless functions in `/api`
  - **Auth**: OAuth endpoints (`/api/auth/`)
  - **Recommendations**: Python-based recommendation engine (`/api/recommendations/`)

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Python, Flask (converted to serverless)
- **Authentication**: Spotify OAuth 2.0
- **AI**: Groq API for natural language processing
- **Deployment**: Vercel
- **Music Data**: Spotify Web API
