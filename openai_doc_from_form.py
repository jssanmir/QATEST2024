from openai import OpenAI 
import json
from PIL import Image
import pytesseract

#load image
image = Image.open('form.jpg')

#Extract text from image
tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
image_to_text = pytesseract.image_to_string(image)
#print(image_to_text)

# call chat completion to generate requirements from a form
client = OpenAI()
role = "You are a SW engineer, skilled in testing complex software systems."
prompt = f"""Please, identify the fields in the following form: [ {image_to_text} ]
        and return only a json format compatible with json parser, without any comment, with the following data 
        [field name][field type][minimum value][maximum value][required][default value] 
        use for maximum, minimum and required the most common choices in the market"""

fields = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": role},
        {"role": "user", 
            "content": prompt}
    ]
)

print(fields.choices[0].message.content)

#iterate over the field structure and read field by field
fields = json.loads(fields.choices[0].message.content)

template = """With the following cases: 
Negative case for value out of minimum limit 
Positive case for minimum limit
Positive case for maximum limit
Negative case for value out of maximum limit
Negative case of missing field if applicable
Negative case of wrong type field
Writing for each case, title in bold, case and expected result"""

for field in fields["fields"]:
    prompt = f"""Please, generate the test cases for the field: [ {field} ]
        applying the following template: {template}"""
    test_cases = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user",
                "content": prompt}
        ]
    )
    print("="*50)
    print(f"Test cases generated for field : {field}")
    print("-"*50)
    print(f"Test Cases:\n{test_cases.choices[0].message.content}\n")