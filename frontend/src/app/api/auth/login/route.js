import { randomBytes } from 'crypto';
import { stringify } from 'querystring';
import { NextResponse } from 'next/server';

const client_id = process.env.SPOTIFY_CLIENT_ID;
const client_secret = process.env.SPOTIFY_CLIENT_SECRET;
const redirect_uri = process.env.VERCEL_URL 
  ? 'https://vibe-check-steel.vercel.app/api/auth/callback'
  : 'http://localhost:3000/api/auth/callback';

const generateRandomString = (length) => {
  return randomBytes(60)
    .toString('hex')
    .slice(0, length);
};

export async function GET() {
  console.log('Client ID:', client_id ? 'Set' : 'NOT SET');
  console.log('Client Secret:', client_secret ? 'Set' : 'NOT SET');
  console.log('Redirect URI:', redirect_uri);

  const state = generateRandomString(16);
  
  console.log('Login - Generated state:', state);

  // Spotify OAuth scope
  const scope = 'user-read-private user-read-email user-library-read playlist-read-private app-remote-control';
  
  const authUrl = 'https://accounts.spotify.com/authorize?' +
    stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    });

  // Create response with redirect and set cookie
  const response = NextResponse.redirect(authUrl);
  
  // Set state cookie
  response.cookies.set('spotify_auth_state', state, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 600,
    path: '/'
  });

  return response;
}
