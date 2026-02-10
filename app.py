import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("Process Review AI - Generate Questions for Process Owners")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload your process Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Read the Excel without headers first
    df_raw = pd.read_excel(uploaded_file, header=None)

    # Extract the table: starts at row 8 (index 7), column 3 (index 2)
    # We will read only relevant columns
    df_table = df_raw.iloc[7:, 2:6]  # Columns C-F (2:6)
    df_table.columns = ["Steps", "Process Steps", "Owner", "Document/Template"]

    # Clean data
    df_table = df_table.dropna(how="all")  # remove empty rows
    df_table["Steps"] = df_table["Steps"].astype(int, errors='ignore')  # ensure Steps is int

    st.subheader("Detected Process Table")
    st.dataframe(df_table)

    # Step 4: Generate questions
    if st.button("Generate Questions for Improvement"):
        st.info("Generating questions... This may take a few seconds.")
        questions_list = []

        for index, row in df_table.iterrows():
            step = row.get("Steps", "")
            process_step = row.get("Process Steps", "")
            owner = row.get("Owner", "")
            document = row.get("Document/Template", "")

            prompt = f"""
You are a business process expert. For the following process step, 
generate a list of targeted, constructive questions to ask the process owner 
to help improve, optimize, or clarify the process. 
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
