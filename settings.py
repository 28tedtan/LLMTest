import streamlit as st

# -------------------- SETTINGS PAGE --------------------
st.title("⚙️ Settings")

st.markdown("---")

# ========== MODEL SETTINGS ==========
st.subheader("Model Configuration")

# Temperature setting
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

temperature = st.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=st.session_state.temperature,
    step=0.1,
    help="Controls randomness: Lower = more focused, Higher = more creative, Default = 0.7"
)
st.session_state.temperature = temperature

# ========== CODE PREFERENCES ==========
st.subheader("Code Preferences")

# Programming language default
if "default_language" not in st.session_state:
    st.session_state.default_language = "Python"

language_options = ["Python", "JavaScript", "Java", "C++", "TypeScript", "Go", "Rust", "Swift"]
default_language = st.selectbox(
    "Default Programming Language",
    language_options,
    index=language_options.index(st.session_state.default_language),
    help="Default language for code generation"
)
st.session_state.default_language = default_language

# Code style
if "code_style" not in st.session_state:
    st.session_state.code_style = "Standard"

code_style = st.radio(
    "Code Style Preference",
    ["Standard", "Minimal Comments", "Heavily Commented", "With Type Hints"],
    index=["Standard", "Minimal Comments", "Heavily Commented", "With Type Hints"].index(st.session_state.code_style),
    help="Choose how you want the generated code to be formatted"
)
st.session_state.code_style = code_style

st.markdown("---")

# ========== UI PREFERENCES ==========
st.subheader("Interface Preferences")

# Theme (note: Streamlit theme is controlled by config, this is just for display)
if "show_line_numbers" not in st.session_state:
    st.session_state.show_line_numbers = True

show_line_numbers = st.checkbox(
    "Show line numbers in code blocks",
    value=st.session_state.show_line_numbers
)
st.session_state.show_line_numbers = show_line_numbers

st.markdown("---")

# ========== DATA MANAGEMENT ==========
st.subheader("Data Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("Clear All History", use_container_width=True, type="secondary"):
        if "conversation_history" in st.session_state:
            st.session_state.conversation_history = []
            st.session_state.has_sent_prompt = False
            st.success("All conversation history cleared!")
        else:
            st.info("No history to clear.")

with col2:
    if st.button("Reset All Settings", use_container_width=True, type="secondary"):
        # Reset to defaults
        st.session_state.temperature = 0.7
        st.session_state.default_language = "Python"
        st.session_state.code_style = "Standard"
        st.session_state.show_line_numbers = True
        st.success("Settings reset to defaults!")
        st.rerun()

st.markdown("---")

# ========== ABOUT ==========
st.subheader("About")
st.markdown("""
**CP Little Helpers** v1.0

A code generation assistant powered by OpenAI's GPT models.

Made for Computing students in Singapore, and worldwide.

Love this project?
""")

st.link_button(
    label="Follow me on Instagram!",
    url="https://www.instagram.com/youfoundted/",
    type="secondary"
)