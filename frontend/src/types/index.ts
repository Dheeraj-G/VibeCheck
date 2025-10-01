export interface Song {
  id: string;
  name: string;
  artist: string;
  album: string;
  imageUrl: string;
}

export interface RecommendationResponse {
  success: boolean;
  songs?: Song[];
  recommendations?: Song[];
  error?: string;
}

export interface PromptRecommendationResponse {
  success: boolean;
  genre?: string;
  artists?: Song[];
  selected?: Song;
  error?: string;
}

export interface TrackInfoResponse {
  id: string;
  name: string;
  artist: string;
  album: string;
  imageUrl: string;
  features?: {
    danceability: number;
    energy: number;
    valence: number;
    tempo: number;
  };
}
