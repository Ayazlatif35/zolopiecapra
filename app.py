import streamlit as st
st.set_page_config(page_title="Secure Name Search", layout="centered")

import pandas as pd
import streamlit_authenticator as stauth

# ----- USER CREDENTIALS -----
usernames = ["user1", "user2", "user3", "user4"]
names = ["User One", "User Two", "User Three", "User Four"]

# CORRECT hashing for your version
hashed_passwords = stauth.Hasher(["test123"] * 4).generate()

# OLD-STYLE credential format (v0.2.x)
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "demo_cookie",
    "demo_key",
    cookie_expiry_days=1
)

# LOGIN
name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Incorrect username or password")
elif auth_status is None:
    st.warning("Please enter your username and password")

# AFTER LOGIN
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
