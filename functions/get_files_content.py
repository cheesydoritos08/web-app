import os
from google.genai import types

MAX_CHARS = 10000


def get_files_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not inside current working directory"

    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f"...File {file_path} was truncated at {MAX_CHARS} chars."
                )

            return file_content_string

    except Exception as e:
        return f"Exception while reading file: {e}"


schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Get the content of the specified file in the specified directory as a string up to a max of 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read the contents from, relative to the working directory. This has to always be provided.",
            ),
        },
    ),
)
