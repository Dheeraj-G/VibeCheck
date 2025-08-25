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

    // For now, return mock data
    // In production, this would call the Python backend
    const mockSongs: Song[] = [
      {
        id: '1',
        name: 'Sweet Child O Mine',
        artist: 'Guns N Roses',
        album: 'Appetite for Destruction',
        imageUrl: '/next.svg',
        popularity: 85,
        externalUrl: 'https://open.spotify.com/track/1'
      },
      {
        id: '2',
        name: 'Wonderwall',
        artist: 'Oasis',
        album: 'Whats the Story Morning Glory',
        imageUrl: '/next.svg',
        popularity: 82,
        externalUrl: 'https://open.spotify.com/track/2'
      },
      {
        id: '3',
        name: 'Smells Like Teen Spirit',
        artist: 'Nirvana',
        album: 'Nevermind',
        imageUrl: '/next.svg',
        popularity: 88,
        externalUrl: 'https://open.spotify.com/track/3'
      },
      {
        id: '4',
        name: 'Creep',
        artist: 'Radiohead',
        album: 'Pablo Honey',
        imageUrl: '/next.svg',
        popularity: 79,
        externalUrl: 'https://open.spotify.com/track/4'
      },
      {
        id: '5',
        name: 'Black',
        artist: 'Pearl Jam',
        album: 'Ten',
        imageUrl: '/next.svg',
        popularity: 81,
        externalUrl: 'https://open.spotify.com/track/5'
      }
    ];

    // TODO: Integrate with Python backend
    // const response = await fetch('http://localhost:5000/recommendations', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ prompt, selectedSong })
    // });
    // const data = await response.json();

    return NextResponse.json({
      success: true,
      songs: mockSongs,
      prompt,
      selectedSong
    });

  } catch (error) {
    console.error('Error processing recommendation request:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
