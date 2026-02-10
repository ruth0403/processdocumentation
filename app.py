import streamlit as st
import pandas as pd

st.title("Process Steps Table Input")

# Define the table structure
columns = ["Step", "Process Steps", "Owner", "Document/Template"]
# Pre-fill Step numbers
data = {"Step": list(range(1, 11)), "Process Steps": ["" for _ in range(10)],
        "Owner": ["" for _ in range(10)], "Document/Template": ["" for _ in range(10)]}

df = pd.DataFrame(data)

# Let user edit the table
edited_df = st.data_editor(df, num_rows="dynamic")

# Display the filled table
st.subheader("Filled Table")
st.dataframe(edited_df)

# Optional: Save the table
if st.button("Save Table"):
    edited_df.to_csv("process_steps.csv", index=False)
    st.success("Table saved as process_steps.csv")
