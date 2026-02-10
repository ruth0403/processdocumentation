import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("Process Review AI - Generate Questions for Process Owners")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload your process Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Step 1: Read the entire Excel without headers
    df_raw = pd.read_excel(uploaded_file, header=None)

    # Step 2: Automatically find the header row
    header_row = None
    expected_headers = ["Steps", "Process Steps", "Owner", "Document/Template"]

    for i, row in df_raw.iterrows():
        if list(row[:4]) == expected_headers:
            header_row = i
            break

    if header_row is None:
        st.error("Could not find the table headers in the Excel file. Make sure it contains Steps, Process Steps, Owner, Document/Template.")
    else:
        # Step 3: Read the table with the correct header
        df = pd.read_excel(uploaded_file, header=header_row)
        df.columns = df.columns.str.strip()  # clean column names
        df.dropna(how="all", inplace=True)   # drop empty rows

        # Ensure Steps column is integer
        if "Steps" in df.columns:
            df["Steps"] = df["Steps"].astype(int, errors='ignore')

        st.subheader("Detected Process Table")
        st.dataframe(df)

        # Step 4: Generate questions
        if st.button("Generate Questions for Improvement"):
            st.info("Generating questions... This may take a few seconds.")
            questions_list = []

            for index, row in df.iterrows():
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
