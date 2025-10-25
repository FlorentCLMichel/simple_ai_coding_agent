import os
import sys
from google import genai
from dotenv import load_dotenv

from functions.schemas import *
from functions.interface import *

system_prompt = '''
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories.
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
'''

max_iterations = 20

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def main():

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
    
    generate_content_loop(client, messages, verbose_mode, working_directory)


def generate_content_loop(client, messages, verbose, working_directory, max_iterations=max_iterations):
    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)

            # Add model response to conversation
            for candidate in response.candidates:
                messages.append(candidate.content)

            # Handle function calls
            if response.function_calls:
                function_responses = []
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose=verbose, working_directory=working_directory)
                    if (
                        not function_call_result.parts
                        or not function_call_result.parts[0].function_response
                    ):
                        raise Exception("empty function call result")
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    function_responses.append(function_call_result.parts[0])
                if function_responses:
                    messages.append(types.Content(role="user", parts=function_responses))
                else:
                    raise Exception("no function responses generated, exiting.")
            else:
                if response.text:
                    print(response.text)
                break
        
        except Exception as e:
            print(f"Error: {e}")
            break
    else:
        print(f"Reached maximum iterations ({max_iterations}). Agent may not have completed the task.")


if __name__ == "__main__":
    main()
