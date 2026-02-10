import streamlit as st
import pandas as pd

st.title("Process Documentation Submission")

# Process metadata
process_name = st.text_input("Process Name:")
process_owner = st.text_input("Process Owner:")

# Create an empty dataframe for steps
steps_df = pd.DataFrame({
    "Steps": [f"Step {i}" for i in range(1, 11)],
    "Process Steps": [""]*10,
    "Owner": [""]*10,
    "Document/Template": [""]*10
})

# Editable table for steps
st.write("### Process Steps")
edited_steps = st.experimental_data_editor(steps_df, num_rows="dynamic")

# Rules
st.write("### Rules")
rules = []
for i in range(1, 6):
    rule = st.text_input(f"Rule {i}", key=f"rule_{i}")
    rules.append(rule)

# Button to export to Excel
if st.button("Export to Excel"):
    # Combine steps and rules into a single Excel
    with pd.ExcelWriter("Process_Documentation.xlsx", engine='xlsxwriter') as writer:
        # Steps sheet
        edited_steps.to_excel(writer, index=False, sheet_name="Steps")
        # Rules sheet
        rules_df = pd.DataFrame({"Rules": rules})
        rules_df.to_excel(writer, index=False, sheet_name="Rules")
    st.success("Excel file saved as 'Process_Documentation.xlsx'")

st.write("### Preview Table")
st.table(edited_steps)
st.write("Rules:", rules)
