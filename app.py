import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

st.set_page_config(page_title="Secure Name Search", layout="centered")

# ---------------- CREDENTIALS ----------------
credentials = {
    "usernames": {
        "user1": {"name": "User One", "password": "test123"},
        "user2": {"name": "User Two", "password": "test123"},
        "user3": {"name": "User Three", "password": "test123"},
        "user4": {"name": "User Four", "password": "test123"},
    }
}

# ---------------- AUTHENTICATOR ----------------
authenticator = stauth.Authenticate(credentials, "demo_cookie", "demo_key")

# ---------------- LOGIN ----------------
name, auth_status, username = authenticator.login("Login", "sidebar")  # <-- fixed

if auth_status is False:
    st.error("Incorrect username or password")
elif auth_status is None:
    st.warning("Please enter your username and password")

# ---------------- APP CONTENT ----------------
if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Logged in as: {name}")

    st.title("🔍 Secure Name Search App")

    df = pd.read_excel("sample_data.xlsx")

    search_name = st.text_input("Enter name to search:")

    if st.button("Search"):
        results = df[df["A"].astype(str).str.contains(search_name, case=False, na=False)]
        if results.empty:
            st.error("No matching records found.")
        else:
            st.success("Record found:")
            st.write(results[["A", "B", "C"]])
