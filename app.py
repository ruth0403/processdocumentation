import streamlit as st
import hashlib
import csv
import os
from datetime import datetime

# ---------------- CONFIG ----------------
LOG_FILE = "usage_log.csv"
REGIONS = ["MEA", "KSA", "EU", "SEA"]

# ---------------- USER DATABASE ----------------
# username: hashed password + default info (position, region)
USER_DB = {
    "alice": {
        "password": hashlib.sha256("alice123".encode()).hexdigest(),
        "position": "HR Manager",
        "region": "MEA"
    },
    "bob": {
        "password": hashlib.sha256("bob123".encode()).hexdigest(),
        "position": "Finance Analyst",
        "region": "EU"
    }
}

# ---------------- LOG FUNCTION ----------------
def log_event(username, action, name="", position="", region=""):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp","username","name","position","region","action"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            username,
            name,
            position,
            region,
            action
        ])

# ---------------- LOGIN FUNCTION ----------------
def login(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    if username in USER_DB and USER_DB[username]["password"] == hashed_pw:
        return True
    return False

# ---------------- INITIALIZE SESSION STATE ----------------
for key in ["logged_in","username","name","position","region"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "logged_in" else False

# ---------------- STREAMLIT APP ----------------
st.title("Internal Authorization System")

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
    st.subheader("User Authorization")

    # User inputs
    name = st.text_input("Name")
    position = st.text_input("Position")
    region = st.selectbox("Region", REGIONS)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    # Validation
    if login_button:
        if not name or not position or not region or not username or not password:
            st.error("All fields are mandatory.")
        elif login(username, password):
            # Save session state
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.name = name
            st.session_state.position = position
            st.session_state.region = region

            log_event(username, "LOGIN", name, position, region)
            st.success(f"Welcome {name} from {region}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

# ---------------- DASHBOARD ----------------
else:
    st.subheader("Dashboard")
    st.write(
        f"Hello {st.session_state.name} ({st.session_state.position}) "
        f"from {st.session_state.region}!"
    )

    st.write("You are logged in. Here you can upload processes, interact with OpenAI, etc.")

    # Example action
    if st.button("Perform Sample Action"):
        log_event(
            st.session_state.username,
            "PERFORMED_SAMPLE_ACTION",
            st.session_state.name,
            st.session_state.position,
            st.session_state.region
        )
        st.success("Sample action logged!")

    # Logout
    if st.button("Logout"):
        log_event(
            st.session_state.username,
            "LOGOUT",
            st.session_state.name,
            st.session_state.position,
            st.session_state.region
        )
        st.session_state.logged_in = False
        st.experimental_rerun()
