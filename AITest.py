from openai import OpenAI
from getpass import getpass
from dotenv import load_dotenv
import os

# set-up
load_dotenv()
api_key = os.getenv("openai_key")
client = OpenAI(api_key=api_key)


#Call model and init
def get_completion(prompt, model="gpt-4o-mini"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1, # this is the degree of randomness of the model's output
    ) 
    return response.choices[0].message.content










#prompt formatting | prompter
prompt = f"""
    Describe xkeyscore
"""


#Response
response = get_completion(prompt)
print(response)