"""
base_agent.py
-------------
Foundation class for all agents.
Contains ONLY the basic setup - nothing else!
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


class BaseAgent:
    """
    Base Agent - Handles API setup
    
    This is the foundation. All other agents inherit from this.
    """
    
    def __init__(self):
        """Initialize Gemini API connection"""
        
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key or api_key == 'your-gemini-api-key-here':
            print("\n❌ ERROR: No valid API key found!")
            print("Please add your Gemini API key to the .env file")
            print("Get free key from: https://makersuite.google.com/app/apikey")
            raise ValueError("Missing API key")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Select model
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("✅ Agent initialized with Gemini\n")

