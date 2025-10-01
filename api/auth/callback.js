const crypto = require('crypto');
const querystring = require('querystring');

const client_id = process.env.SPOTIFY_CLIENT_ID;
const client_secret = process.env.SPOTIFY_CLIENT_SECRET;
const redirect_uri = process.env.VERCEL_URL 
  ? `https://${process.env.VERCEL_URL}/api/auth/callback`
  : 'http://localhost:3000/api/auth/callback';

export default function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const code = req.query.code || null;
  const state = req.query.state || null;
  const storedState = req.cookies?.spotify_auth_state;

  console.log('Callback received - State from URL:', state);
  console.log('Callback received - Stored state from cookie:', storedState);

  if (state === null || state !== storedState) {
    console.log('State mismatch detected!');
    return res.redirect('/?' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  }

  // Clear the state cookie
  res.setHeader('Set-Cookie', 'spotify_auth_state=; HttpOnly; Secure; SameSite=Lax; Max-Age=0; Path=/');

  const authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    form: {
      code: code,
      redirect_uri: redirect_uri,
      grant_type: 'authorization_code'
    },
    headers: {
      'content-type': 'application/x-www-form-urlencoded',
      Authorization: 'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64')
    },
    json: true
  };

  // Use fetch instead of request library for serverless
  const tokenUrl = 'https://accounts.spotify.com/api/token';
  const tokenData = new URLSearchParams({
    code: code,
    redirect_uri: redirect_uri,
    grant_type: 'authorization_code'
  });

  fetch(tokenUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64')
    },
    body: tokenData
  })
  .then(response => response.json())
  .then(body => {
    console.log('Token request response:', body);
    
    if (body.access_token) {
      const access_token = body.access_token;
      const refresh_token = body.refresh_token;

      // Redirect to the frontend with the access token
      res.redirect('/?' +
        querystring.stringify({
          access_token: access_token,
          refresh_token: refresh_token
        }));
    } else {
      console.log('Token request failed:', body);
      res.redirect('/?' +
        querystring.stringify({
          error: 'invalid_token'
        }));
    }
  })
  .catch(error => {
    console.error('Token request error:', error);
    res.redirect('/?' +
      querystring.stringify({
        error: 'token_request_failed'
      }));
  });
}
