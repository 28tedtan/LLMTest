import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os


# -------------------- SETUP ------------------------
load_dotenv()
api_key = os.getenv("openai_key")
client = OpenAI(api_key=api_key)


# -------------------- RESPONSE MODEL ----------------
class CodeResponse(BaseModel):
    code: str
    explanation: str


# -------------------- COMPLETION FUNCTION -----------
def get_completion(prompt, model="gpt-4o-mini"):

    messages = [
#---------------------- Prompt Engineering------------
        {"role": "system", "content": """
You are a helpful programming assistant.
You are to generate PYTHON code for user
- code: the generated code
- explanation: a simple explanation of the code and have KEYWORDS and explain along the way if deemed necessary.
Imagine you are talking to middle schoolers and make it that simple to make them understand
"""},
#------------------------------------------------------


        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=CodeResponse
    )

    return response.choices[0].message.parsed







# -------------------- STREAMLIT UI -------------------
st.title("CP little helper")

user_prompt = st.text_area("Enter a prompt")

if st.button("Generate Code"):
    if not user_prompt:
        st.error("Please enter a prompt.")
    else:
        # Optional token safety
        if len(user_prompt) > 3000:
            st.error("You are wasting too many tokens, rejected.")
        else:
            result = get_completion(user_prompt)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Generated Code")
                st.code(result.code, language="python", line_numbers=True)

            with col2:
                st.subheader("Explanation")
                st.write(result.explanation)