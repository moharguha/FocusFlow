import streamlit as st # type: ignore
from utils.db import conn, c

def login():
    st.subheader("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        
        result = c.fetchone()

        if result:
            st.session_state.user = user
            st.session_state.premium = result[2]
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

def signup():
    st.subheader("Signup")

    user = st.text_input("New Username")
    pwd = st.text_input("New Password", type="password")

    if st.button("Create Account"):
       c.execute("INSERT INTO users (username, password, premium) VALUES (?, ?, ?)", (user, pwd, 0))
       conn.commit()
       st.success("Account created!")
