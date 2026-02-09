import streamlit as st
import streamlit_authenticator as stauth

# User credentials
names = ["Alice", "Bob"]
usernames = ["alice", "bob"]
passwords = ["pass1", "pass2"]  # you can hash passwords

authenticator = stauth.Authenticate(
    names, usernames, passwords,
    "app_cookie", "signature_key"
)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status:
    st.write(f"Welcome {name}")
    # Place your chat interface here
elif auth_status is False:
    st.error("Username/password is incorrect")
else:
    st.warning("Please enter your credentials")
