from openai import OpenAI 
import json


# Read the JSON file called "mqtt protocol.json"
with open('mqtt protocol.json', 'r') as file:
    protocol = json.load(file)

role = "You are a SW engineer, skilled in testing complex software systems."

template = """With the following cases:
    Negative case for value out of minimum limit
    Positive case for minimum limit
    Positive case
    Negative case for value out of maximum limit
    Positive case for maximum limit
    Negative case of missing field if applicable
    Negative case of wrong type field"""


client = OpenAI()

for property in protocol["properties"]:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", 
             "content": f"Please, Write the test cases for field {property} taking into account the following protocol specifications {protocol}, applying the following template: {template} ,"}
        ]
          
    )
    test_cases = completion.choices[0].message.content
    print("="*50)
    print(f"Test cases generated for field : {property}")
    print("-"*50)
    print(f"Test Cases:\n{test_cases}\n")
    