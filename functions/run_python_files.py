import os
import subprocess
from google.genai import types


def run_python_files(working_directory: str, file_path: str, args: list = []):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not inside current working directory"

    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"

    if not file_path.endswith(".py"):
        return f"Error {file_path} is not a python file"

    try:
        final_args = ["python3", file_path]
        final_args.extend(args)
        output = subprocess.run(
            final_args, timeout=30.0, capture_output=True, cwd=abs_working_dir
        )

        if output is None:
            return "No output produced"

        final_string = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
        """

        if output.returncode != 0:
            final_string += f"Process exited with return code: {output.returncode}"

        return final_string
    except Exception as e:
        return f"Exception while running file {file_path}: {e}"


schema_run_python_files = types.FunctionDeclaration(
    name="run_python_files",
    description="Runs a python file with the python3 interpreter. Accepts additional CLI  arguments as an optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run , relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The optional array of strings to be used as the command line arguments for the python file",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)
