import streamlit as st
import yaml
import pandas as pd
from datetime import datetime
import os

# -------------------------
# Config
# -------------------------
st.set_page_config(page_title="Secure App", layout="centered")

LOG_FILE = "login_logs.csv"

# -------------------------
# Load users
# -------------------------
with open("users.yaml") as f:
    users = yaml.safe_load(f)["users"]

# -------------------------
# Initialize log file
# -------------------------
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "timestamp", "name", "position", "region", "username"
    ]).to_csv(LOG_FILE, index=False)

# -------------------------
# Session state
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

# -------------------------
# Login Function
# -------------------------
def login():
    st.title("🔐 Authorized Login")

    name = st.text_input("Name")
    position = st.text_input("Position")
    region = st.selectbox("Region", ["MEA", "KSA", "EU", "SEA"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not all([name, position, region, username, password]):
            st.error("All fields are mandatory.")
            return

        if username in users and users[username]["password"] == password:
            # Authenticate
            st.session_state.authenticated = True
            st.session_state.user_role = users[username]["role"]
            st.session_state.username = username

            # Log login
            log_entry = pd.DataFrame([{
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name,
                "position": position,
                "region": region,
                "username": username
            }])

            log_entry.to_csv(LOG_FILE, mode="a", header=False, index=False)

            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# -------------------------
# Main App
# -------------------------
def main_app():
    st.title("🏠 Main Application")

    st.write(f"Welcome **{st.session_state.username}** 👋")

    st.info("You are now inside the secured app.")

    # Admin-only logs
    if st.session_state.user_role == "admin":
        st.subheader("📊 Login Activity (Admin Only)")
        logs = pd.read_csv(LOG_FILE)
        st.dataframe(logs, use_container_width=True)

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# -------------------------
# App Flow
# -------------------------
if not st.session_state.authenticated:
    login()
else:
    main_app()
