import streamlit as st
import streamlit_authenticator as stauth

# ---- Step 1: Define users ----
names = ["Alice", "Bob"]
usernames = ["alice", "bob"]
passwords = ["password123", "securepass456"]  # optional: hash passwords for more security

# ---- Step 2: Initialize authenticator ----
authenticator = stauth.Authenticate(
    names,
    usernames,
    passwords,
    "cookie_name",        # cookie name for session
    "signature_key",      # secret key
    cookie_expiry_days=1
)

# ---- Step 3: Login UI ----
name, auth_status, username = authenticator.login("Login", "main")

# ---- Step 4: Handle authentication ----
if auth_status:
    st.success(f"Welcome {name}!")
    
    # Example protected content
    st.write("This is internal content only accessible to authorized users.")
    
    # Add logout button
    if st.button("Logout"):
        authenticator.logout("main")
        st.experimental_rerun()

elif auth_status is False:
    st.error("Username/password incorrect")
else:
    st.warning("Please enter your credentials")
