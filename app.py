import streamlit as st
import pandas as pd
from pptx import Presentation
from transformers import pipeline

# Free LLM pipeline
question_gen = pipeline("text2text-generation", model="meta-llama/Llama-2-7b-chat-hf")

st.title("Free SOP Automation Portal")

# 1. Collect SOP
process_name = st.text_input("Process Name")
owner = st.text_input("Owner")
steps = st.text_area("Steps")

if st.button("Submit SOP"):
    # Check for missing fields
    missing = []
    if not process_name: missing.append("Process Name")
    if not owner: missing.append("Owner")
    if not steps: missing.append("Steps")

    if missing:
        st.warning(f"Missing fields: {missing}")
        # Generate clarifying questions
        prompt = f"Generate questions for missing fields {missing} in this SOP: {process_name}, {owner}, {steps}"
        questions = question_gen(prompt, max_length=200)
        st.write("Clarifying Questions:")
        st.info(questions[0]['generated_text'])
    else:
        st.success("SOP submitted successfully!")

# 2. Optional PPT generation here with python-pptx
