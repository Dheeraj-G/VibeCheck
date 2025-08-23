"use client";

import Image from "next/image";
import { useSearchParams, useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Page() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  useEffect(() => {
    const accessToken = searchParams.get('access_token');
    const refreshToken = searchParams.get('refresh_token');
    
    if (accessToken && refreshToken) {
      // Store tokens securely (you can use localStorage, sessionStorage, or state management)
      localStorage.setItem('spotify_access_token', accessToken);
      localStorage.setItem('spotify_refresh_token', refreshToken);
      
      // Redirect to clean URL without tokens
      router.replace('/');
    }
  }, [searchParams, router]);
  
  return (
    <div className="min-h-screen bg-black text-white">
      <h1>Hello World</h1>
      <p>Welcome to VibeCheck!</p>
    </div>
  );
}
