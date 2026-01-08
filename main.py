import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import time


# -------------------- SETUP ------------------------
load_dotenv()
api_key = os.getenv("openai_key")
client = OpenAI(api_key=api_key)

# Load training instructions from external file
with open(".traininginstructions", "r") as f:
    training_instructions = f.read()


# -------------------- RESPONSE MODEL ----------------
class CodeResponse(BaseModel):
    code: str
    explanation: str


# -------------------- COMPLETION FUNCTION -----------
def get_completion(prompt, model="gpt-4o-mini"):

    messages = [
#---------------------- Prompt Engineering------------
        {"role": "system", "content": training_instructions},
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
st.title("CP AI generator")

# Persist chat input attributes across reruns
# Start with the initial prompt label; after first submit we flip to "Follow up".
if "chattext" not in st.session_state:
    st.session_state.chattext = "Enter a coding prompt"
if "disabledtext" not in st.session_state:
    st.session_state.disabledtext = False
if "has_sent_prompt" not in st.session_state:
    st.session_state.has_sent_prompt = False

# Once a prompt has been sent, make the label permanently "Follow up"
if st.session_state.has_sent_prompt:
    st.session_state.chattext = "Follow up"

chattext = st.session_state.chattext
disabledtext = st.session_state.disabledtext

user_prompt = st.chat_input(chattext, disabled=disabledtext, max_chars=3000)

if user_prompt:
    # Optional token safety 2nd wave type shi
    if len(user_prompt) > 3000:
        st.error("You are wasting too many tokens, rejected. How are you even doing this...")
    else:
        # Keep chat input attributes consistent across reruns
        st.session_state.chattext = "Follow up"
        st.session_state.disabledtext = False
        # Status

        with st.status("Thinking...", expanded=False) as status:
            starttime = time.perf_counter()
            result = get_completion(user_prompt)
            endtime = time.perf_counter()

            elapsed_seconds = endtime - starttime  
            elapsed_int = int(round(elapsed_seconds))  
            st.session_state["last_response_time_s"] = elapsed_int

            if  elapsed_seconds > 60:
                status.update(label="Taking a while...")

            st.toast("Completed!", icon="✅")

            status.update(
                label=f"Completed               ({elapsed_seconds:.1f}s)" 
            )
            disabledtext = False


        #code generation
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Generated Code")
            st.code(result.code, language="python", line_numbers=True)

        with col2:
            st.subheader("Explanation")
            st.write(result.explanation)