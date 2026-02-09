import streamlit as st
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

st.title("Process Submission & Validation")

# Step 1: Upload process Excel
uploaded_file = st.file_uploader("Upload Process Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Uploaded process:")
    st.dataframe(df)

    if st.button("Validate Process"):
        # Step 2: Send process to OpenAI for questions
        process_text = df.to_dict(orient="records")
        prompt = f"""
        You are a process reviewer. Here is the employee-submitted process:
        {process_text}
        Ask questions for missing or unclear steps. Return JSON of questions.
        """
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        questions = response.choices[0].message.content
        st.write("OpenAI Questions:")
        st.json(questions)

        # Step 3: Collect employee answers dynamically
        answers = {}
        for q in eval(questions):  # assuming questions is a JSON string
            answers[q["step"]] = st.text_input(f"Step {q['step']} - {q['question']}")

        if st.button("Submit Answers"):
            # Step 4: Send answers back to OpenAI for final process
            prompt_update = f"""
            Update the following process based on employee answers:
            Process: {process_text}
            Answers: {answers}
            Return updated process in JSON format.
            """
            response_final = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt_update}],
            )
            updated_process = response_final.choices[0].message.content
            st.write("Updated Process:")
            st.json(updated_process)
