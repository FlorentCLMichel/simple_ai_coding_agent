import os
import sys
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.schemas import *
from functions.interface import *

# Constants
API_KEY_NAME = "GEMINI_API_KEY"
MODEL_NAME = "MODEL"
DEFAULT_MODEL = "gemini-2.0-flash-001"
DEFAULT_MAX_ITERATIONS = 20
DEFAULT_MAX_TOKENS = 10000
SYS_PROMPT_FILE = "system_prompt.txt"

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_create_dir,
        schema_write_file,
        schema_move_file,
        schema_run_python_file,
        schema_cc,
        schema_cxx,
    ]
)

def main():
    """Main function to run the AI coding agent."""

    parser = argparse.ArgumentParser(description="An experimental AI coding agent.")
    parser.add_argument("prompt", help="The user prompt.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose mode.")
    parser.add_argument("--work_dir", default="temp", help="Working directory.")
    parser.add_argument("--max_iter", default=str(DEFAULT_MAX_ITERATIONS), help="Maximum number of iterations.")
    parser.add_argument("--max_tok", default=str(DEFAULT_MAX_TOKENS), 
                        help="Maximum number of tokens. WARNING: The actual number of tokens used may exceed this value.")
    parser.add_argument("--sys_prompt", default=str(SYS_PROMPT_FILE), help="File with the system prompt.")
    parser.add_argument("--usr_prompt", default=None, help="File with the user prompt (will override prompt).")

    args = parser.parse_args()

    verbose_mode = args.verbose
    working_directory = args.work_dir
    if args.usr_prompt:
        with open(args.usr_prompt, 'r') as file:
            user_prompt = file.read()
    else:
        user_prompt = args.prompt
    try:
        max_iterations = int(args.max_iter)
        if max_iterations <= 0:
            raise ValueError("max_iter must be a positive integer.")
    except ValueError as e:
        print(f"Error: Invalid max_iter value: {e}")
        sys.exit(1)
    try:
        max_tokens = int(args.max_tok)
        if max_iterations <= 0:
            raise ValueError("max_tok must be a positive integer.")
    except ValueError as e:
        print(f"Error: Invalid max_tok value: {e}")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get(API_KEY_NAME)
    model = os.environ.get(MODEL_NAME)

    if not api_key:
        print(f"ERROR: {API_KEY_NAME} not set")
        sys.exit(1)

    if not model:
        print(f"ERROR: {MODEL_NAME} not set")
        sys.exit(1)

    # Create working directory if it doesn't exist
    if not os.path.isdir(working_directory):
        os.makedirs(working_directory, exist_ok=True)

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content_loop(client, model, messages, verbose_mode, working_directory, max_iterations, max_tokens)

def load_system_prompt(file_path=SYS_PROMPT_FILE):
    with open(file_path, "r") as f:
        return f.read()

def call_api(client, model, messages, available_functions, system_instruction):
    """Calls the Gemini API and returns the response."""
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_instruction
        ),
    )
    return response

def handle_function_calls(response, verbose, working_directory):
    """Handles function calls in the API response."""
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
    return function_responses

def generate_content_loop(client, model, messages, verbose, working_directory, max_iterations, max_tokens):
    system_instruction = load_system_prompt()
    total_tokens = 0
    for iteration in range(max_iterations):
        if total_tokens >= max_tokens:
            print(f"Reached or exceeded maximum number of tokens ({max_tokens}). Agent may not have completed the task.")
            break
        
        try:
            response = call_api(client, model, messages, available_functions, system_instruction)
            total_tokens += response.usage_metadata.prompt_token_count
            total_tokens += response.usage_metadata.candidates_token_count

            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
                print("Total number of tokens used:", total_tokens)

            # Add model response to conversation
            for candidate in response.candidates:
                messages.append(candidate.content)

            # Handle function calls
            if response.function_calls:
                function_responses = handle_function_calls(response, verbose, working_directory)
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
