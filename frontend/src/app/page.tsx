"use client";

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Image from "next/image";

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
  const [naturalLanguagePrompt, setNaturalLanguagePrompt] = useState('');
  const [selectedSong, setSelectedSong] = useState<Song | null>(null);
  const [suggestedSongs, setSuggestedSongs] = useState<Song[]>([]);
  const [spotifySuggestions, setSpotifySuggestions] = useState<Song[]>([]);
  const [showSpotifyDropdown, setShowSpotifyDropdown] = useState(false);
  
  useEffect(() => {
    const accessToken = searchParams.get('access_token');
    const refreshToken = searchParams.get('refresh_token');
    
    if (accessToken && refreshToken) {
      localStorage.setItem('spotify_access_token', accessToken);
      localStorage.setItem('spotify_refresh_token', refreshToken);
      router.replace('/');
    }
  }, [searchParams, router]);

  // Mock data for demonstration - replace with actual API calls
  const mockSpotifySuggestions: Song[] = [
    { id: '1', name: 'Bohemian Rhapsody', artist: 'Queen', album: 'A Night at the Opera', imageUrl: '/next.svg' },
    { id: '2', name: 'Hotel California', artist: 'Eagles', album: 'Hotel California', imageUrl: '/next.svg' },
    { id: '3', name: 'Stairway to Heaven', artist: 'Led Zeppelin', album: 'Led Zeppelin IV', imageUrl: '/next.svg' },
  ];

  const mockSuggestedSongs: Song[] = [
    { id: '4', name: 'Sweet Child O Mine', artist: 'Guns N Roses', album: 'Appetite for Destruction', imageUrl: '/next.svg' },
    { id: '5', name: 'Wonderwall', artist: 'Oasis', album: 'Whats the Story Morning Glory', imageUrl: '/next.svg' },
    { id: '6', name: 'Smells Like Teen Spirit', artist: 'Nirvana', album: 'Nevermind', imageUrl: '/next.svg' },
    { id: '7', name: 'Creep', artist: 'Radiohead', album: 'Pablo Honey', imageUrl: '/next.svg' },
    { id: '8', name: 'Black', artist: 'Pearl Jam', album: 'Ten', imageUrl: '/next.svg' },
  ];

  useEffect(() => {
    setSuggestedSongs(mockSuggestedSongs);
  }, []);

  const handleSpotifySearch = (value: string) => {
    setSpotifySearch(value);
    if (value.length > 2) {
      setSpotifySuggestions(mockSpotifySuggestions.filter(song => 
        song.name.toLowerCase().includes(value.toLowerCase()) ||
        song.artist.toLowerCase().includes(value.toLowerCase())
      ));
      setShowSpotifyDropdown(true);
    } else {
      setShowSpotifyDropdown(false);
    }
  };

  const handleSongSelect = (song: Song) => {
    setSelectedSong(song);
    setSpotifySearch(`${song.name} - ${song.artist}`);
    setShowSpotifyDropdown(false);
  };

  const handleNaturalLanguageSearch = async () => {
    if (!naturalLanguagePrompt.trim()) return;
    
    try {
      const response = await fetch('/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: naturalLanguagePrompt,
          selectedSong: selectedSong?.id
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setSuggestedSongs(data.songs);
      }
    } catch (error) {
      console.error('Error getting recommendations:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black text-white">
      {/* Top Section - Search Bars */}
      <div className="h-1/3 p-8 flex flex-col justify-center items-center space-y-6">
        <div className="w-full max-w-2xl relative">
          <input
            type="text"
            placeholder="Search for songs on Spotify..."
            value={spotifySearch}
            onChange={(e) => handleSpotifySearch(e.target.value)}
            className="w-full px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
          {showSpotifyDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-black/90 backdrop-blur-sm border border-white/20 rounded-lg max-h-60 overflow-y-auto z-10">
              {spotifySuggestions.map((song) => (
                <div
                  key={song.id}
                  onClick={() => handleSongSelect(song)}
                  className="px-4 py-3 hover:bg-white/10 cursor-pointer border-b border-white/10 last:border-b-0"
                >
                  <div className="font-medium">{song.name}</div>
                  <div className="text-sm text-white/70">{song.artist} • {song.album}</div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <div className="w-full max-w-2xl flex space-x-4">
          <input
            type="text"
            placeholder="Describe the vibe you're looking for..."
            value={naturalLanguagePrompt}
            onChange={(e) => setNaturalLanguagePrompt(e.target.value)}
            className="flex-1 px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
          <button
            onClick={handleNaturalLanguageSearch}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 rounded-lg font-medium transition-all duration-200 transform hover:scale-105"
          >
            Get Recommendations
          </button>
        </div>
      </div>

      {/* Middle Section - Selected Song Display */}
      <div className="h-1/3 p-8 flex flex-col justify-center items-center">
        {selectedSong ? (
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-6 text-center max-w-md">
              {selectedSong.name}
            </h2>
            <div className="w-48 h-48 mx-auto relative">
              <Image
                src={selectedSong.imageUrl}
                alt={`${selectedSong.album} album cover`}
                fill
                className="rounded-lg object-cover shadow-2xl"
              />
            </div>
            <p className="mt-4 text-white/80">{selectedSong.artist}</p>
            <p className="text-white/60">{selectedSong.album}</p>
          </div>
        ) : (
          <div className="text-center text-white/60">
            <div className="w-48 h-48 mx-auto bg-white/10 rounded-lg flex items-center justify-center border-2 border-dashed border-white/20">
              <span className="text-lg">Select a song to see details</span>
            </div>
          </div>
        )}
      </div>

      {/* Bottom Section - Song Suggestions Carousel */}
      <div className="h-1/3 p-8">
        <h3 className="text-xl font-semibold mb-6 text-center">Recommended Songs</h3>
        <div className="flex space-x-6 overflow-x-auto pb-4 scrollbar-hide">
          {suggestedSongs.map((song) => (
            <div key={song.id} className="flex-shrink-0 text-center group cursor-pointer">
              <div className="w-32 h-32 relative mb-3 group-hover:scale-105 transition-transform duration-200">
                <Image
                  src={song.imageUrl}
                  alt={`${song.album} album cover`}
                  fill
                  className="rounded-lg object-cover shadow-lg"
                />
              </div>
              <h4 className="font-medium text-sm mb-1 group-hover:text-purple-300 transition-colors">
                {song.name}
              </h4>
              <p className="text-xs text-white/70">{song.artist}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
