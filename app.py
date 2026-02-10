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
1. Enter the process name and your name.  
2. Copy your Excel table (with headers: Steps, Process Steps, Owner, Document/Template) and paste it below.  
3. Enter the process rules in the separate text area.  
4. AI will generate improvement questions for each step considering the rules.  
5. Ensure your process submission has answers to all the improvement questions incorporated in it.
""")

# --- Process metadata ---
col1, col2 = st.columns(2)

with col1:
    process_name = st.text_input("Process Name")

with col2:
    submitter_name = st.text_input("Submitted By")

# --- Step 1: Paste table ---
table_input = st.text_area(
    "Paste your process table here (with headers)",
    height=300
)

# --- Step 2: Enter rules separately ---
rules_input = st.text_area(
    "Enter process rules here (each rule on a new line)",
    height=150
)

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

    # Ensure Steps column format
    if "Steps" in df.columns:
        df["Steps"] = df["Steps"].astype(str)

    st.subheader("Process Table Preview")
    st.dataframe(df, use_container_width=True)

    # Prepare rules for AI
    rules_text = rules_input.strip()

    if rules_text:
        st.subheader("Process Rules")
        st.write(rules_text)

    # --- Step 3: Generate AI questions ---
    if st.button("Generate Improvement Questions"):
        if not process_name or not submitter_name:
            st.error("Please enter both Process Name and Submitted By before proceeding.")
        elif not rules_text:
            st.error("Please enter at least one process rule.")
        else:
            st.info("Generating questions... This may take a few seconds...")
            questions_list = []

            # Convert table to text for AI
            table_text = df.to_string(index=False)

            prompt = f"""
You are a Process Documentation Reviewer.

Process Name: {process_name}
Submitted By: {submitter_name}

Process Table:
{table_text}

Process Rules:
{rules_text}

Task:
- For EACH process step, generate 1–2 improvement or clarification questions.
- Questions must check compliance with the rules.
- Do NOT rewrite steps.
- Do NOT add new steps.
- Number questions by step number.
- Be precise and professional.
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in SOP and process governance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            st.subheader("AI Improvement Questions")
            st.write(response.choices[0].message.content)
