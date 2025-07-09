import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your API key from .env file
load_dotenv()

# Configure the client with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use a supported model name from the list
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

# Generate content
response = model.generate_content("Tell me a mind-blowing fact about the universe.")

# Print the result
print(response.text)
