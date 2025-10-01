'use client';
import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Image from 'next/image';

interface Song {
  id: string;
  name: string;
  artist: string;
  album: string;
  imageUrl: string;
}

export default function Page() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const [spotifySearch, setSpotifySearch] = useState('');
  const [selectedSong, setSelectedSong] = useState<Song | null>(null);
  const [spotifySuggestions, setSpotifySuggestions] = useState<Song[]>([]);
  const [showSpotifyDropdown, setShowSpotifyDropdown] = useState(false);
  const [suggestedSongs, setSuggestedSongs] = useState<Song[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = searchParams.get('access_token');
    const refresh = searchParams.get('refresh_token');
    if (token && refresh) {
      localStorage.setItem('spotify_access_token', token);
      localStorage.setItem('spotify_refresh_token', refresh);
      router.replace('/');
    }
  }, [searchParams, router]);

  // Prompt-based recommendations (via backend Groq -> genre -> artists)
  const fetchPromptRecommendations = async (prompt: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const userToken = localStorage.getItem('spotify_access_token');
      const res = await fetch("http://localhost:5001/prompt_recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt,
          userToken: userToken
        }),
      });
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`API error: ${res.status} - ${errorText}`);
      }
      const data = await res.json();
      // data: { success, genre, artists: Song[], selected: Song }
      setSelectedSong(data.selected || null);
      setSuggestedSongs(data.artists || []);
    } catch (err) {
      console.error("Error fetching prompt recommendations:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch prompt recommendations");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchRecommendations = async (song: Song) => {
    setIsLoading(true);
    setError(null);
    try {
      const userToken = localStorage.getItem('spotify_access_token');
      const res = await fetch("http://localhost:5001/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          songId: song.id,
          userToken: userToken  // Send user's Spotify token
        }),
      });
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`API error: ${res.status} - ${errorText}`);
      }
      const data = await res.json();
      console.log("Song-based recommendations:", data.songs || data.recommendations || []);
      setSuggestedSongs(data.songs || data.recommendations || []);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setError(err instanceof Error ? err.message : "Failed to fetch recommendations");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSpotifySearch = async (value: string) => {
    setSpotifySearch(value);
    // No dropdown; treat input as prompt. Trigger on Enter instead.
    setShowSpotifyDropdown(false);
  };

  const handlePromptSubmit = () => {
    if (spotifySearch.trim().length === 0) return;
    fetchPromptRecommendations(spotifySearch.trim());
  };

  const handleSongSelect = (song: Song) => {
    setSelectedSong(song);
    setSpotifySearch(`${song.name} - ${song.artist}`);
    setShowSpotifyDropdown(false);
    console.log('Selected song:', JSON.stringify(song, null, 2));
    fetchRecommendations(song);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black text-white">
      {/* Top Section - Search */}
      <div className="p-8 flex flex-col items-center space-y-6">
        <div className="w-full max-w-2xl relative mb-6">
          <input
            type="text"
            placeholder="Describe a vibe or mood (e.g., upbeat summer road trip)"
            value={spotifySearch}
            onChange={(e) => handleSpotifySearch(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') handlePromptSubmit(); }}
            className="w-full px-4 py-3 bg-white/10 rounded-lg text-white placeholder-white/60 focus:outline-none"
          />
          <div className="mt-3 flex justify-end">
            <button
              onClick={handlePromptSubmit}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded-md text-sm font-medium"
            >
              Get Artists
            </button>
          </div>
        </div>
      </div>

      {/* Middle Section - Selected Artist (from prompt) */}
      <div className="p-8 flex flex-col items-center">
        {selectedSong ? (
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-6">{selectedSong.name}</h2>
            <div className="w-48 h-48 relative mb-4">
              {selectedSong.imageUrl ? (
                <Image src={selectedSong.imageUrl} alt={selectedSong.name} fill className="rounded-lg object-cover" />
              ) : (
                <div className="w-full h-full bg-white/10 rounded-lg flex items-center justify-center">
                  <span className="text-white/50">No Image</span>
                </div>
              )}
            </div>
            <p className="text-white/80">{selectedSong.artist}</p>
            {selectedSong.album ? (
              <p className="text-white/60">{selectedSong.album}</p>
            ) : null}
          </div>
        ) : (
          <div className="text-white/60">
            <div className="w-48 h-48 bg-white/10 rounded-lg border-dashed border-white/20 flex items-center justify-center">
              <span>Enter a prompt to get artists</span>
            </div>
          </div>
        )}
      </div>

      {/* Bottom Section - Recommended Artists */}
      <div className="p-8">
        <h3 className="text-xl font-semibold mb-6 text-center">Recommended Artists</h3>
        
        {error && (
          <div className="text-center mb-6">
            <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 max-w-md mx-auto">
              <p className="text-red-300 font-medium">Error loading recommendations</p>
              <p className="text-red-200 text-sm mt-1">{error}</p>
            </div>
          </div>
        )}
        
        {isLoading && (
          <div className="text-center mb-6">
            <div className="inline-flex items-center space-x-2 text-white/70">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Loading recommendations...</span>
            </div>
          </div>
        )}
        
        <div className="flex justify-center flex-wrap gap-6">
          {suggestedSongs.length > 0 ? (
            suggestedSongs.map((song) => (
              <div key={song.id} className="flex-shrink-0 text-center group cursor-pointer">
                <div className="w-32 h-32 relative mb-3 group-hover:scale-105 transition-transform duration-200">
                  {song.imageUrl ? (
                    <Image src={song.imageUrl} alt={song.name} fill className="rounded-lg object-cover shadow-lg" />
                  ) : (
                    <div className="w-full h-full bg-white/10 rounded-lg flex items-center justify-center">
                      <span className="text-white/40 text-xs">No Image</span>
                    </div>
                  )}
                </div>
                <h4 className="font-medium text-sm mb-1 group-hover:text-purple-300 transition-colors">
                  {song.name}
                </h4>
                <p className="text-xs text-white/70">{song.artist}</p>
              </div>
            ))
          ) : !isLoading && !error ? (
            <p className="text-white/50">No recommendations yet — enter a prompt above.</p>
          ) : null}
        </div>
      </div>
    </div>
  );
}
