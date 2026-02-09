import streamlit as st
import streamlit_authenticator as stauth
import yaml

# -------------------------
# Step 1: Define users
# -------------------------
# For demonstration, passwords are hashed. DO NOT store plain text passwords in production.

users = {
    "usernames": {
        "ruthu": {
            "name": "Ruthu",
            "password": stauth.Hasher(["mypassword123"]).generate()[0]
        },
        "admin": {
            "name": "Admin",
            "password": stauth.Hasher(["adminpass"]).generate()[0]
        }
    }
}

# -------------------------
# Step 2: Initialize authenticator
# -------------------------
authenticator = stauth.Authenticate(
    users["usernames"],
    "streamlit_app_cookie",  # cookie name
    "random_signature_key",  # key for encryption
    cookie_expiry_days=1
)

# -------------------------
# Step 3: Login widget
# -------------------------
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}!")
    
    # Your main app content goes here
    st.write("This is a secure page. Only authorized users can see this.")
    
    # Add a logout button
    authenticator.logout("Logout", "main")

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
