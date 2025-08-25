#!/usr/bin/env python3
"""
Simple test script for Groq API integration
"""

import os
from dotenv import load_dotenv
from song_recommendations import SongRecommendationsEngine

def test_groq_integration():
    """Test the Groq API integration"""
    print("🧪 Testing Groq API Integration")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key or api_key == 'your_groq_api_key_here':
        print("❌ GROQ_API_KEY not set in .env file")
        print("Please add your Groq API key to .env file")
        return False
    
    try:
        # Initialize the engine
        print("📡 Initializing SongRecommendationsEngine...")
        engine = SongRecommendationsEngine()
        
        if not engine.groq_client:
            print("❌ Groq client not available")
            return False
        
        # Test simple API call
        print("🔍 Testing simple API call...")
        test_response = engine._call_groq_api(
            "Say hello in one word",
            max_tokens=10
        )
        
        if test_response:
            print(f"✅ API call successful: {test_response}")
        else:
            print("❌ API call failed")
            return False
        
        # Test natural language processing
        print("🎵 Testing natural language processing...")
        result = engine.process_natural_language_prompt(
            "I want energetic rock music for working out"
        )
        
        if result and 'energy' in result:
            print("✅ Natural language processing successful")
            print(f"   Extracted features: {result}")
        else:
            print("❌ Natural language processing failed")
            return False
        
        print("\n🎉 All tests passed! Groq API integration is working.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_groq_integration()
    exit(0 if success else 1)
