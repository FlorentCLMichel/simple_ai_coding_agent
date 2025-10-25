from google.genai import types

from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False, working_directory='.'):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    if function_call_part.name in functions.keys():
        function_args["working_directory"] = working_directory
        function_result = functions[function_name](**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
