import streamlit as st
import pandas as pd
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Process Review AI - Generate Questions for Process Owners")

# Upload Excel
uploaded_file = st.file_uploader("Upload your process Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Process Table")
    st.dataframe(df)

    if st.button("Generate Questions for Improvement"):
        st.info("Generating questions... This may take a few seconds.")
        questions_list = []

        # Iterate through rows to create prompts for AI
        for index, row in df.iterrows():
            step = row.get("Step", "")
            process_step = row.get("Process Steps", "")
            owner = row.get("Owner", "")
            document = row.get("Document/Template", "")

            # Build a prompt for AI
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
                max_tokens=250
            )

            questions = response.choices[0].message["content"]
            questions_list.append((step, process_step, questions))

        # Display the questions
        st.subheader("Generated Questions")
        for step, process_step, questions in questions_list:
            st.markdown(f"**Step {step}: {process_step}**")
            st.markdown(questions)
            st.write("---")

        # Optionally export to Excel
        export_df = pd.DataFrame(questions_list, columns=["Step", "Process Step", "Questions"])
        export_df.to_excel("process_questions.xlsx", index=False)
        st.success("Questions exported as process_questions.xlsx")
