import { NextResponse } from 'next/server';

const client_id = process.env.SPOTIFY_CLIENT_ID;
const client_secret = process.env.SPOTIFY_CLIENT_SECRET;

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const refresh_token = searchParams.get('refresh_token');

  if (!refresh_token) {
    return NextResponse.json({ error: 'refresh_token required' }, { status: 400 });
  }

  const tokenUrl = 'https://accounts.spotify.com/api/token';
  const tokenData = new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: refresh_token
  });

  try {
    const response = await fetch(tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + Buffer.from(client_id + ':' + client_secret).toString('base64')
      },
      body: tokenData
    });

    const body = await response.json();
    
    if (body.access_token) {
      return NextResponse.json({
        access_token: body.access_token,
        refresh_token: body.refresh_token || refresh_token
      });
    } else {
      return NextResponse.json({ error: 'Failed to refresh token' }, { status: 400 });
    }
  } catch (error) {
    console.error('Refresh token error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
