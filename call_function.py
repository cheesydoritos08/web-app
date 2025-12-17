from functions.get_files_info import get_files_info
from functions.get_files_content import get_files_content
from functions.write_files import write_files
from functions.run_python_files import run_python_files
from google.genai import types

WORKING_DIRECTORY = "calculator"


def call_function(function_call_part, verbose: bool = False):
    if verbose:
        print(f"Calling function {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function {function_call_part.name}")

    result = ""
    if function_call_part.name == "get_files_content":
        result = get_files_content(
            working_directory=WORKING_DIRECTORY,
            **function_call_part.args,
        )
    if function_call_part.name == "write_files":
        result = write_files(
            working_directory=WORKING_DIRECTORY,
            **function_call_part.args,
        )

    if function_call_part.name == "get_files_info":
        result = get_files_info(
            working_directory=WORKING_DIRECTORY,
            **function_call_part.args,
        )
        
    if function_call_part.name == "run_python_files":
        result = run_python_files(
            working_directory=WORKING_DIRECTORY,
            **function_call_part.args,
        )



    if result == "":
        return types.Content(
            role="tool",
            parts=types.Part.from_function_response(
                name=function_call_part.name,
                response={f"Error: Unknown function {function_call_part.name}"},
            ),
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
            name=function_call_part.name, 
            response={"result": result}
        )
        ],
    )
