import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
