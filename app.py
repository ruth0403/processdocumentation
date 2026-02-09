import streamlit as st
import hashlib

# ----------------- USER DATABASE -----------------
# Store usernames and hashed passwords
USER_DB = {
    "alice": hashlib.sha256("alice123".encode()).hexdigest(),
    "bob": hashlib.sha256("bob123".encode()).hexdigest()
}

# ----------------- LOGIN FUNCTION -----------------
def login(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    if username in USER_DB and USER_DB[username] == hashed_pw:
        return True
    return False

# ----------------- APP START -----------------
st.title("Internal Streamlit App Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if login(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password")
else:
    st.subheader("Dashboard")
    st.write("You are logged in! Here you can upload processes, interact with OpenAI, etc.")
    
    logout_button = st.button("Logout")
    if logout_button:
        st.session_state.logged_in = False
        st.experimental_rerun()
