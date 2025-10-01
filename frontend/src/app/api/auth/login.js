import { randomBytes } from 'crypto';
import { stringify } from 'querystring';

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

export default function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  console.log('Client ID:', client_id ? 'Set' : 'NOT SET');
  console.log('Client Secret:', client_secret ? 'Set' : 'NOT SET');
  console.log('Redirect URI:', redirect_uri);

  const state = generateRandomString(16);
  
  // Set state cookie
  res.setHeader('Set-Cookie', `spotify_auth_state=${state}; HttpOnly; Secure; SameSite=Lax; Max-Age=600; Path=/`);

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

  res.redirect(authUrl);
}
