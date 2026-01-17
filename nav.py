import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Computing Little Helpers",
    page_icon="",
    layout="wide"
)

# -------------------- NAVIGATION --------------------
# Create navigation with pages
page = st.navigation([
    st.Page("main.py", title="Chat"),
    st.Page("settings.py", title="Settings", icon="⚙️"),
])

# Run the selected page
page.run()