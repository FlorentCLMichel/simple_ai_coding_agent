import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("MODEL")

client = genai.Client(api_key=api_key)

if (len(sys.argv) < 2) or ("--help" in sys.argv[1:]) or ("-h" in sys.argv[1]) :
    print("Use: python3 main.py <promt> <options>")
    print("Options:")
    print("  --help, -h    : Display this help message")
    print("  --verbose, -v : Verbose mode")
    exit(1)

verbose_mode = ("--verbose" in sys.argv[1:]) or ("-v" in sys.argv[1:])

user_prompt = sys.argv[1]

messages = [
    genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model=model,
    contents=messages)
print(response.text)

if verbose_mode : 
    print("")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
