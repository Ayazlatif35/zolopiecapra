# app.py
import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Secure Name Search", layout="centered")

# ---------------- CREDENTIALS ----------------
usernames = ["user1", "user2", "user3", "user4"]
names = ["User One", "User Two", "User Three", "User Four"]
passwords = ["test123"] * 4  # plain passwords for demonstration

# ---------------- HASH PASSWORDS ----------------
hashed_passwords = stauth.Hasher(passwords).hash()

credentials = {
    "usernames": {
        uname: {"name": name, "password": pwd}
        for uname, name, pwd in zip(usernames, names, hashed_passwords)
    }
}

# ---------------- AUTHENTICATOR ----------------
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="demo_cookie",
    key="demo_key",
    cookie_expiry_days=1
)

# ---------------- LOGIN ----------------
name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Incorrect username or password")
elif auth_status is None:
    st.warning("Please enter your username and password")

# ---------------- APP CONTENT ----------------
if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Logged in as: {name}")

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
