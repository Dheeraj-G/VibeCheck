import { NextResponse } from 'next/server';
import { SongRecommendationsEngine } from '../../../../lib/song_engine';

// Initialize engine globally
const engine = new SongRecommendationsEngine();

export async function POST(req: Request) {
  try {
    const { prompt, userToken } = await req.json();
    
    if (!prompt) {
      return NextResponse.json({ success: false, error: "Prompt is required" }, { status: 400 });
    }

    const result = await engine.getPromptRecommendations(prompt, userToken);
    
    if (!result.success) {
      return NextResponse.json(result, { status: 400 });
    }

    return NextResponse.json({
      success: true,
      genre: result.genre,
      artists: result.artists,
      selected: result.selected,
    });

  } catch (err: unknown) {
    console.error('Error in prompt recommendations API:', err);
    const errorMessage = err instanceof Error ? err.message : 'Internal server error';
    return NextResponse.json({ 
      success: false, 
      error: errorMessage
    }, { status: 500 });
  }
}
