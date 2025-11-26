# app.py
import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Secure Name Search", layout="centered")



st.title("🔍 Secure Name Search App")

    # Make sure your Excel file exists in the repo
    df = pd.read_excel("sample_data.xlsx")  
    search_name = st.text_input("Enter name to search:")

    if st.button("Search"):
        results = df[df["A"].astype(str).str.contains(search_name, case=False, na=False)]
        if results.empty:
            st.error("No matching records found.")
        else:
            st.success("Record found:")
            st.dataframe(results[["A", "B", "C"]])  # nicely formatted table
