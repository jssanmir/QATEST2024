
from openai import OpenAI 
import json

# Define the list of requirements
requirements = [
    "The system should allow users to create an account",
    "The system should allow users to log in and log out",
    "The system should allow users to upload files",
    "The system should allow users to download files",
    "The system should allow users to share files with other users"
]
role = "You are a SW engineer, skilled in testing complex software systems."
template = "Test case ID, Test case description, test case steps, and expected result in bold" 
client = OpenAI()

# Call OpenAI to generate test cases for each requirement
for requirement in requirements:
    prompt = f"Generate test cases for the following requirement: {requirement}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", 
             "content": f"Please, write the test cases required to cover the following {requirement}, applying the following template: {template} ,"
            }
        ]
    )
    
    
    test_cases = completion.choices[0].message.content
    print("="*50)
    print(f"Requirement: {requirement}")
    print("-"*50)
    print(f"Test Cases:\n{test_cases}\n")
