import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("MODEL")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2 :
    print("Missing argument: Prompt")
    exit(1)

user_prompt = sys.argv[1]

messages = [
    genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model=model,
    contents=messages)
print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
