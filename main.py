import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import time

# -------------------- SETUP ------------------------
load_dotenv()
api_key = os.getenv("openai_key")

# api_key = st.secrets["openai_key"]
client = OpenAI(api_key=api_key)

# Load training instructions from external file
with open(".traininginstructions", "r") as f:
    training_instructions = f.read()

# -------------------- RESPONSE MODEL ----------------
class CodeResponse(BaseModel):
    code: str
    explanation: str

# -------------------- COMPLETION FUNCTION -----------
def get_completion(prompt, conversation_history, model="gpt-4o-mini"):
    # Build messages with conversation history
    messages = [
        {"role": "system", "content": training_instructions}
    ]

    # Add conversation history
    for entry in conversation_history:
        messages.append({"role": "user", "content": entry["prompt"]})
        messages.append({"role": "assistant", "content": f"Code:\n{entry['code']}\n\nExplanation:\n{entry['explanation']}"})
    
    # Add current prompt
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=CodeResponse
    )

    return response.choices[0].message.parsed

# -------------------- STREAMLIT UI -------------------
st.title("CP Little Helpers")

# ========== CONVERSATION HISTORY ==========
# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Persist chat input attributes across reruns
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

# ========== DISPLAY CONVERSATION HISTORY ==========
# Display all conversation entries FIRST (no chat bubbles, just clean display)
if st.session_state.conversation_history:
    st.markdown("---")
    
    for idx, entry in enumerate(st.session_state.conversation_history):
        
        # Code and explanation in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Generated Code")
            st.code(entry['code'], language="python", line_numbers=True)
            
            # Download button for this code
            st.download_button(
                label="📥 Download Code",
                data=entry['code'],
                file_name=f"generated_code_{idx + 1}.py",
                mime="text/plain",
                key=f"download_{idx}"
            )
        
        with col2:
            st.subheader("Explanation")
            st.write(entry['explanation'])
        
        # Separator between entries
        if idx < len(st.session_state.conversation_history) - 1:
            st.markdown("---")
    
    # ========== CONVERSATION CONTROLS ==========
    # Add new chat button at the bottom if there's history
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.has_sent_prompt = False
            st.session_state.chattext = "Enter a coding prompt"
            st.rerun()

# ========== CENTERED WELCOME MESSAGE ==========
# Only show if NO prompts have been sent yet
if not st.session_state.has_sent_prompt:
    # Center the welcome message
    st.markdown("""
        <div style='text-align: center; margin-top: 150px; margin-bottom: 50px;'>
            <h2 style='color: #666; font-weight: 300;'>What would you like to learn today?</h2>
        </div>
    """, unsafe_allow_html=True)

# Chat input is ALWAYS visible at the bottom
user_prompt = st.chat_input(chattext, disabled=disabledtext, max_chars=3000)

if user_prompt:
    # Mark that a prompt has been sent IMMEDIATELY
    st.session_state.has_sent_prompt = True
    
    # Optional token safety
    if len(user_prompt) > 3000:
        st.error("You are wasting too many tokens, rejected. How are you even doing this...")
    else:
        # Keep chat input attributes consistent across reruns
        st.session_state.chattext = "Follow up"
        st.session_state.disabledtext = False
        
        # ========== LOADING ANIMATIONS ==========
        with st.status("Thinking...", expanded=False) as status:
            starttime = time.perf_counter()
            result = get_completion(user_prompt, st.session_state.conversation_history)
            endtime = time.perf_counter()

            elapsed_seconds = endtime - starttime  
            elapsed_int = int(round(elapsed_seconds))  
            st.session_state["last_response_time_s"] = elapsed_int

            if elapsed_seconds > 60:
                status.update(label="⏳ Taking a while...")

            status.update(
                label=f"✓ Completed ({elapsed_seconds:.1f}s)" 
            )
            
            st.toast("Completed!", icon="✅")
            
            disabledtext = False
        
        # ========== STORE IN CONVERSATION HISTORY ==========
        st.session_state.conversation_history.append({
            "prompt": user_prompt,
            "code": result.code,
            "explanation": result.explanation,
            "timestamp": time.time()
        })
        
        # Rerun to show the new entry
        st.rerun()
    