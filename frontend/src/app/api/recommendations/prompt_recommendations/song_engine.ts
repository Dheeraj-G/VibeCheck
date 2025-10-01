import SpotifyWebApi from 'spotify-web-api-node';
import Groq from 'groq-sdk';

export interface Song {
  id: string;
  name: string;
  artist: string;
  album: string;
  imageUrl: string;
  popularity: number;
}

export class SongRecommendationsEngine {
  private spotifyClient: SpotifyWebApi | null = null;
  private groqClient: Groq | null = null;
  private allowedGenres: Set<string> = new Set();

  constructor() {
    this.initializeSpotifyClient();
    this.initializeGroqClient();
    this.loadGenres();
  }

  private initializeSpotifyClient(): void {
    try {
      const clientId = process.env.SPOTIFY_CLIENT_ID;
      const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;

      if (!clientId || !clientSecret) {
        console.warn('Spotify credentials not found in environment variables.');
        return;
      }

      this.spotifyClient = new SpotifyWebApi({
        clientId,
        clientSecret,
      });

      // Get client credentials
      this.spotifyClient.clientCredentialsGrant().then(
        (data) => {
          this.spotifyClient!.setAccessToken(data.body.access_token);
          console.log('Spotify client initialized successfully.');
        },
        (err) => {
          console.error('Error initializing Spotify client:', err);
        }
      );
    } catch (error) {
      console.error('Error initializing Spotify client:', error);
    }
  }

  private initializeGroqClient(): void {
    try {
      const apiKey = process.env.GROQ_API_KEY;
      if (!apiKey) {
        console.warn('Groq API key not found in environment variables.');
        return;
      }

      this.groqClient = new Groq({
        apiKey,
      });
      console.log('Groq client initialized successfully.');
    } catch (error) {
      console.error('Error initializing Groq client:', error);
    }
  }

  private loadGenres(): void {
    // For now, we'll use a basic set of genres
    // In a real implementation, you'd load this from a file or API
    this.allowedGenres = new Set([
      'pop', 'rock', 'hip-hop', 'electronic', 'jazz', 'classical',
      'country', 'r&b', 'reggae', 'blues', 'folk', 'indie'
    ]);
    console.log(`Loaded ${this.allowedGenres.size} Spotify genres.`);
  }

  private async getSpotifyClientWithUserToken(userToken?: string): Promise<SpotifyWebApi | null> {
    if (!userToken) {
      console.log('No user token provided, using client credentials');
      return this.spotifyClient;
    }

    try {
      const userSpotifyClient = new SpotifyWebApi();
      userSpotifyClient.setAccessToken(userToken);
      
      // Test the token by making a simple API call
      await userSpotifyClient.getMe();
      console.log('Successfully created Spotify client with user token');
      return userSpotifyClient;
    } catch (error) {
      console.warn('Failed to create user Spotify client:', error);
      return this.spotifyClient;
    }
  }

  private normalizeGenre(text: string): string | null {
    if (!text) return null;
    const textLower = text.trim().toLowerCase();
    const normalized = textLower.split(',')[0].split('\n')[0].trim().replace(/[.\s]+$/, '');
    return normalized || null;
  }

  async getGenreFromPrompt(prompt: string): Promise<string | null> {
    if (!this.groqClient) {
      return null;
    }

    try {
      const model = process.env.GROQ_MODEL || 'llama-3.1-8b-instant';
      const allowedGenresList = Array.from(this.allowedGenres).sort();

      const fullPrompt = `
        You are a music genre selector. Your job is to imagine what the user prompt would be like and choose the best fitting genre.
        Return exactly one genre from this list and do not invent new genres: ${allowedGenresList.join(', ')}.
        Return only the genre name from the list. If unsure, respond with "none".
        No extra words, no explanations. Example: "pop", not "Pop music".

        User said: "${prompt}"

        Respond with exactly one genre name from the list only.
      `;

      const completion = await this.groqClient.chat.completions.create({
        model,
        messages: [{ role: 'user', content: fullPrompt }],
        temperature: 0.2,
        max_tokens: 8,
        top_p: 1,
        stream: false,
      });

      const content = completion.choices[0].message.content?.trim().toLowerCase() || '';
      const normalized = this.normalizeGenre(content);
      
      // Check if the normalized genre is in our allowed list
      if (normalized && this.allowedGenres.has(normalized)) {
        return normalized;
      }
      
      return null;
    } catch (error) {
      console.warn('Groq genre extraction failed:', error);
      return null;
    }
  }

  async findArtistsByGenre(genre: string, userToken?: string, limit: number = 6): Promise<Song[]> {
    const spotifyClient = await this.getSpotifyClientWithUserToken(userToken);
    if (!spotifyClient) {
      console.error('No Spotify client available');
      return [];
    }

    try {
      const query = `genre:"${genre}"`;
      const searchResult = await spotifyClient.searchArtists(query, { limit: 50 });
      const artistItems = searchResult.body.artists?.items || [];
      
      const results: Song[] = [];
      for (const artist of artistItems) {
        if (!artist) continue;
        
        const popularity = artist.popularity || 0;
        const imageUrl = artist.images?.[0]?.url || '';
        
        results.push({
          id: artist.id,
          name: artist.name,
          artist: genre,
          album: '',
          imageUrl,
          popularity
        });
        
        if (results.length >= limit) break;
      }
      
      return results;
    } catch (error) {
      console.error('Spotify API error finding artists by genre:', error);
      return [];
    }
  }

  async getPromptRecommendations(prompt: string, userToken?: string): Promise<{
    success: boolean;
    genre?: string;
    artists?: Song[];
    selected?: Song;
    error?: string;
  }> {
    try {
      if (!prompt) {
        return { success: false, error: 'Prompt is required' };
      }

      const genre = await this.getGenreFromPrompt(prompt);
      if (!genre) {
        return { success: false, error: 'Could not derive genre from prompt' };
      }

      const artists = await this.findArtistsByGenre(genre, userToken, 6);
      if (!artists.length) {
        return { success: false, error: `No artists found for genre '${genre}'` };
      }

      return {
        success: true,
        genre,
        artists,
        selected: artists[0]
      };
    } catch (error) {
      console.error('Error in getPromptRecommendations:', error);
      return { success: false, error: 'Internal server error' };
    }
  }
}
