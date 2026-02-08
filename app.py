import streamlit as st
import pandas as pd

st.title("SOP Submission Portal")

process_name = st.text_input("Process Name")
owner = st.text_input("Owner")
steps = st.text_area("Steps")
inputs = st.text_input("Inputs")
outputs = st.text_input("Outputs")

if st.button("Submit"):
    df = pd.DataFrame([{
        "Process Name": process_name,
        "Owner": owner,
        "Steps": steps,
        "Inputs": inputs,
        "Outputs": outputs
    }])
    df.to_excel("submissions.xlsx", index=False)
    st.success("SOP Submitted!")
