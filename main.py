import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("MODEL")

client = genai.Client(api_key=api_key)

# Test that we can communicate with the model
response = client.models.generate_content(
    model=model,
    contents="Hi! What's the date today?")
print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
