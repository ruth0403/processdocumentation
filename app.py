import streamlit as st
import streamlit_authenticator as stauth

# ---- Authentication ----
names = ["Alice"]
usernames = ["alice"]
passwords = ["password123"]  # for security, you can hash these

authenticator = stauth.Authenticate(
    names, usernames, passwords,
    "cookie_name", "signature_key"
)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status:
    st.write(f"Welcome {name}!")

    # ---- Chat in RAM only ----
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Enter your message:")

    if user_input:
        # For now, AI just echoes back
        response = f"Echo: {user_input}"
        st.session_state.messages.append({"user": user_input, "bot": response})

    # Display chat
    for chat in st.session_state.messages:
        st.write(f"**User:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")

    if st.button("Clear Chat"):
        st.session_state.messages = []

elif auth_status is False:
    st.error("Username/password incorrect")
else:
    st.warning("Please enter your credentials")
