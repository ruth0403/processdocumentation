import streamlit as st
import pandas as pd
from io import StringIO
from openai import OpenAI

st.set_page_config(page_title="Process Review AI", layout="wide")
st.title("Process Review AI - Table + Rules Analysis")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.markdown("""
**Instructions:**  
1. Copy your Excel table (with headers: Steps, Process Steps, Owner, Document/Template) and paste it below.  
2. Enter the process rules in the separate text area.  
3.Improvement questions will be generated.
4. Ensure your process submission has answers to all the improvement questions incorporated in it.
""")

# --- Step 1: Paste table ---
table_input = st.text_area("Paste your process table here (with headers)", height=300)

# --- Step 2: Enter rules separately ---
rules_input = st.text_area("Enter process rules here (each rule on a new line)", height=150)

if table_input:
    # Try reading table as tab-separated, fallback to comma
    try:
        df = pd.read_csv(StringIO(table_input), sep="\t")
    except:
        df = pd.read_csv(StringIO(table_input))

    # Clean headers
    df.columns = df.columns.str.strip()

    # Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)

    # Ensure Steps column is integer
    if "Steps" in df.columns:
        df["Steps"] = df["Steps"].astype(int, errors="ignore")

    st.subheader("Process Table Preview")
    st.dataframe(df)

    # Prepare rules for AI
    rules_text = rules_input.strip().replace("\n", "; ")

    if rules_text:
        st.subheader("Process Rules")
        st.write(rules_text)

    # --- Step 3: Generate AI questions ---
    if st.button("Generate Improvement Questions"):
        st.info("Generating questions... This may take a few seconds...")
        questions_list = []
