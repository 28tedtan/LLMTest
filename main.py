import streamlit as st
from openai import OpenAI
from getpass import getpass
from dotenv import load_dotenv
from pydantic import BaseModel
import os




# set-up ######################################################################################################################
load_dotenv()
api_key = os.getenv("openai_key")
client = OpenAI(api_key=api_key)


#response model ###############################################################################################################
class CodeResponse(BaseModel):
    code: str
    explanation: str





###########################################################################################################################################################################################
#MAIN CODE ######################################################################################### MAIN CODE ############################################################################
st.title("OpenAI Codex")


user_prompt = st.text_area("Enter a prompt")
if user_prompt: get_completion()

st.code(result.code, language=result.language.lower())

st.frame()


















# END OF MAIN CODE #############################################################################################################################################################################
################################################################################################################################################################################################


#Call model and init ##########################################################################################################
def get_completion(prompt, model="gpt-4o-mini"):
    messages = [
        {"role": "user", "content": user_prompt}
        #system prompt ##########################################################################################################
        {"role": "system", "content": """- You are a helpful assistant that can help writing code in most programming languages such as Python, JavaScript, HTML, CSS, SQL, SwiftUI, React, etc.
        You must give clear and concise instructions to the user.
        Comments in code are highly encouraged and beneficial to the user.
        after the code is written, you should explain the code to the user in a way that is easy to understand outside of the code block."""
    }

        ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format: CodeResponse
    )
    if message.parsed:
        result = message.parsed










#Response #########################################################################################
response = get_completion(prompt)
print(response)

