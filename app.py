import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Secure Name Search", layout="centered")

# ---------------- CREDENTIALS ----------------
# Very old v0.2.x requires a credentials dictionary
credentials = {
    "usernames": {
        "user1": {"name": "User One", "password": "test123"},
        "user2": {"name": "User Two", "password": "test123"},
        "user3": {"name": "User Three", "password": "test123"},
        "user4": {"name": "User Four", "password": "test123"},
    }
}

# ---------------- AUTHENTICATOR ----------------
# Old constructor: credentials dict, cookie name, key
authenticator = stauth.Authenticate(credentials, "demo_cookie", "demo_key")

# ---------------- LOGIN ----------------
# Use 'sidebar' instead of 'main' (allowed values: 'sidebar', 'unrendered')
name, auth_status, username = authenticator.login("Login", "sidebar")

if auth_status is False:
    st.error("Incorrect username or password")
elif auth_status is None:
    st.warning("Please enter your username and password")

# ---------------- APP CONTENT ----------------
if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Logged in as: {name}")

    st.title("🔍 Secure Name Search App")

    # Load Excel data
    df = pd.read_excel("sample_data.xlsx")  # Make sure this file exists

    search_name = st.text_input("Enter name to search:")

    if st.button("Search"):
        # Case-insensitive search in column 'A'
        results = df[df["A"].astype(str).str.contains(search_name, case=False, na=False)]
        if results.empty:
            st.error("No matching records found.")
        else:
            st.success("Record found:")
            st.write(results[["A", "B", "C"]])
