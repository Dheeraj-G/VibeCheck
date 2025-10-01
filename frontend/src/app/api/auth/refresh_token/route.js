const client_id = process.env.SPOTIFY_CLIENT_ID;
const client_secret = process.env.SPOTIFY_CLIENT_SECRET;

export default function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const refresh_token = req.query.refresh_token;

  if (!refresh_token) {
    return res.status(400).json({ error: 'refresh_token required' });
  }

  const tokenUrl = 'https://accounts.spotify.com/api/token';
  const tokenData = new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: refresh_token
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
    if (body.access_token) {
      res.json({
        access_token: body.access_token,
        refresh_token: body.refresh_token || refresh_token
      });
    } else {
      res.status(400).json({ error: 'Failed to refresh token' });
    }
  })
  .catch(error => {
    console.error('Refresh token error:', error);
    res.status(500).json({ error: 'Internal server error' });
  });
}
