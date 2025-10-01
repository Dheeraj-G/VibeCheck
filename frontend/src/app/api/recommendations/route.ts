import { NextRequest, NextResponse } from 'next/server';

interface RecommendationRequest {
  prompt: string;
  selectedSong?: string;
}

interface Song {
  id: string;
  name: string;
  artist: string;
  album: string;
  imageUrl: string;
  popularity: number;
  externalUrl: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: RecommendationRequest = await request.json();
    const { prompt, selectedSong } = body;

    if (!prompt) {
      return NextResponse.json(
        { error: 'Prompt is required' },
        { status: 400 }
      );
    }

    // Call the Python backend
    try {
      const response = await fetch('http://localhost:5001/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ songId: selectedSong })
      });
      
      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }
      
      const data = await response.json();
      return NextResponse.json(data);
    } catch (error) {
      console.error('Error calling backend:', error);
      return NextResponse.json(
        { error: 'Failed to get recommendations from backend' },
        { status: 500 }
      );
    }

  } catch (error) {
    console.error('Error processing recommendation request:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
