import os
import sys
from google import genai
from dotenv import load_dotenv

from functions.schemas import *
from functions.interface import *

system_prompt = '''
You are a helpful AI coding agent.
When a user asks a question or makes a request, you may either provide a direct answer or make a function call plan. You can perform the following operations:
- List files and directories.
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
'''

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model = os.environ.get("MODEL")

client = genai.Client(api_key=api_key)

if (len(sys.argv) < 2) or ("--help" in sys.argv[1:]) or ("-h" in sys.argv[1]) :
    print("Use: python3 main.py <prompt> <options>")
    print("Options:")
    print("  --help, -h      : Display this help message")
    print("  --verbose, -v   : Verbose mode")
    print("  --work_dir <wd> : Working directory")
    exit(1)

verbose_mode = ("--verbose" in sys.argv[1:]) or ("-v" in sys.argv[1:])
if "--work_dir" in sys.argv[1:]:
    working_directory = sys.argv[sys.argv.index("--work_dir")+1]
else:
    working_directory = "test_calculator"

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
        function_call_result = call_function(function_call, verbose=verbose_mode, working_directory=working_directory)
        if verbose_mode:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)

if verbose_mode : 
    print("")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
