# setup_test.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content("Test message: Can you confirm you are working?")

print("Gemini API response:\n", response.text)
