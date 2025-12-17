import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_files_content
from functions.write_files import schema_write_files
from functions.run_python_files import schema_run_python_files
from call_function import call_function

def main():
    # Loads the AI into the environment
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Sets up system prompt
    system_prompt: str = os.environ.get("SYSTEM_PROMPT")

    # Lists available functions for agent to use
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_write_files,
            schema_run_python_files,
        ]
    )

    #
    config = types.GenerateContentConfig(
        system_instruction=system_prompt, tools=[available_functions]
    )

    # Checks to see if a prompt was given
    if len(sys.argv) < 2:
        return print("I need a prompt")

    is_verbose = False

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        is_verbose = True


    # Sends the prompt to the AI and generates a response
    prompt = sys.argv[1]
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    max_iters = 20
    for i in range(0,  max_iters):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=messages, config=config
        )

        # Checks if a function was called
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part=function_call_part, verbose=is_verbose)
                messages.append(result)
               
        else:
            # Checks if verbose flag is present
            if is_verbose:
                print(f"Prompt: {prompt}")
                print(f"Prompt token: {response.usage_metadata.prompt_token_count}")
                print(f"Response token: {response.usage_metadata.candidates_token_count}")
                
            print(response.text)
            return


main()
