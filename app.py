import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="Process Review AI", layout="wide")
st.title("Process Review AI - Generate Questions for Process Owners")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Upload Excel
uploaded_file = st.file_uploader("Upload your process Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Read Excel without headers first
    df_raw = pd.read_excel(uploaded_file, header=None)

    # Extract relevant columns: starts from row 8 (index 7), column 3 (index 2)
    df_section = df_raw.iloc[7:, 2:6]  # Columns C-F
    df_section.columns = ["Steps", "Process Steps", "Owner", "Document/Template"]

    # Drop fully empty rows
    df_section = df_section.dropna(how="all").reset_index(drop=True)

    # Find the row where "Rules" appears in Process Steps
    rules_index = df_section[df_section["Process Steps"].astype(str).str.strip().str.lower() == "rules"].index

    if len(rules_index) > 0:
        rules_index = rules_index[0]
        # Split table and rules
        df_table = df_section.iloc[:rules_index].copy()
        df_rules = df_section.iloc[rules_index + 1 :].copy()  # everything after "Rules"
        rules_text = "; ".join(df_rules["Process Steps"].dropna().astype(str).tolist())
    else:
        df_table = df_section.copy()
        rules_text = ""

    # Ensure Steps column is integer
    df_table["Steps"] = df_table["Steps"].astype(int, errors="ignore")

    st.subheader("Detected Process Table")
    st.dataframe(df_table)

    if rules_text:
        st.subheader("Detected Rules (considered for AI questions)")
        st.write(rules_text)

    # Generate AI questions
    if st.button("Generate Improvement Questions"):
        st.info("Generating questions... This may take a few seconds...")
        questions_list = []

        for _, row in df_table.iterrows():
            step = row.get("Steps", "")
            process_step = row.get("Process Steps", "")
            owner = row.get("Owner", "")
            document = row.get("Document/Template", "")

            prompt = f"""
You are a business process expert.
Here are the process rules: {rules_text}

For the following process step, generate a list of targeted, constructive questions
to ask the process owner to improve, optimize, or clarify the process.
Do not answer the questions, only list them.

Step: {step}
Process Step: {process_step}
Owner: {owner}
Document/Template: {document}
"""

            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400
            )

            questions = response.choices[0].message["content"]
            questions_list.append((step, process_step, questions))

        # Display questions
        st.subheader("Generated Questions")
        for step, process_step, questions in questions_list:
            st.markdown(f"**Step {step}: {process_step}**")
            st.markdown(questions)
            st.write("---")

        # Export to Excel
        export_df = pd.DataFrame(questions_list, columns=["Step", "Process Step", "Questions"])
        export_df.to_excel("process_questions.xlsx", index=False)
        st.success("Questions exported as process_questions.xlsx")
