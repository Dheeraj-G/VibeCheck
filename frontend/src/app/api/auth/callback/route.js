import { stringify } from 'querystring';
import { NextResponse } from 'next/server';

const client_id = process.env.SPOTIFY_CLIENT_ID;
const client_secret = process.env.SPOTIFY_CLIENT_SECRET;
const redirect_uri = process.env.VERCEL_URL 
  ? 'https://vibe-check-steel.vercel.app/api/auth/callback'
  : 'http://localhost:3000/api/auth/callback';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');
  const state = searchParams.get('state');
  
  // Get cookies from request
  const cookieStore = request.cookies;
  const storedState = cookieStore.get('spotify_auth_state')?.value;

  console.log('Callback received - State from URL:', state);
  console.log('Callback received - Stored state from cookie:', storedState);

  if (state === null || state !== storedState) {
    console.log('State mismatch detected!');
    return NextResponse.redirect(new URL('/?' + stringify({
      error: 'state_mismatch'
    }), request.url));
  }

  // Use fetch instead of request library for serverless
  const tokenUrl = 'https://accounts.spotify.com/api/token';
  const tokenData = new URLSearchParams({
    code: code,
    redirect_uri: redirect_uri,
    grant_type: 'authorization_code'
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
    console.log('Token request response:', body);
    
    if (body.access_token) {
      const access_token = body.access_token;
      const refresh_token = body.refresh_token;

      // Create response with redirect and clear cookie
      const redirectResponse = NextResponse.redirect(new URL('/?' + stringify({
        access_token: access_token,
        refresh_token: refresh_token
      }), request.url));
      
      // Clear the state cookie
      redirectResponse.cookies.set('spotify_auth_state', '', {
        httpOnly: true,
        secure: true,
        sameSite: 'lax',
        maxAge: 0,
        path: '/'
      });
      
      return redirectResponse;
    } else {
      console.log('Token request failed:', body);
      return NextResponse.redirect(new URL('/?' + stringify({
        error: 'invalid_token'
      }), request.url));
    }
  } catch (error) {
    console.error('Token request error:', error);
    return NextResponse.redirect(new URL('/?' + stringify({
      error: 'token_request_failed'
    }), request.url));
  }
}
