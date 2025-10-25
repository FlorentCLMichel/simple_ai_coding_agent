import os
import sys
from google import genai
from dotenv import load_dotenv

from functions.schemas import *

system_prompt = '''
You are a helpful AI coding agent.
When a user asks a question or makes a request, you may either provide a direct answer or make a function call plan. You can perform the following operations:
- List files and directories.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
'''

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("MODEL")

client = genai.Client(api_key=api_key)

if (len(sys.argv) < 2) or ("--help" in sys.argv[1:]) or ("-h" in sys.argv[1]) :
    print("Use: python3 main.py <prompt> <options>")
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
    contents=messages,
    config=genai.types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt),
    )
if response.function_calls is not None:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print(response.text)

if verbose_mode : 
    print("")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
