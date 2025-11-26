import streamlit as st
st.set_page_config(page_title="Secure Name Search", layout="centered")

import pandas as pd
import streamlit_authenticator as stauth

# ----- USER CREDENTIALS -----
usernames = ["user1", "user2", "user3", "user4"]
names = ["User One", "User Two", "User Three", "User Four"]

# HASH PASSWORDS (new API)
passwords = ["test123"] * 4
hashed_passwords = stauth.Hasher().hash(passwords)

# CREDENTIAL DICTIONARY (new API)
credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "password": hashed_passwords[i]
        }
        for i in range(len(usernames))
    }
}

# AUTHENTICATOR OBJECT (new API)
authenticator = stauth.Authenticate(
    credentials,
    "demo_cookie",
    "demo_key",
    cookie_expiry_days=1
)

# ----- LOGIN -----
name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Incorrect username or password")
elif auth_status is None:
    st.warning("Please enter your username and password")

# ----- APPLICATION AFTER LOGIN -----
if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Logged in as: {name}")

    st.title("🔍 Secure Name Search App")

    # Load Excel File
    df = pd.read_excel("sample_data.xlsx")

    search_name = st.text_input("Enter name to search:")

    if st.button("Search"):
        results = df[df["A"].astype(str).str.contains(search_name, case=False, na=False)]
        if results.empty:
            st.error("No matching records found.")
        else:
            st.success("Record found:")
            st.write(results[["A", "B", "C"]])
