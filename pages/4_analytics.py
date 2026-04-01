import streamlit as st
import pandas as pd
from utils.db import conn

st.title("📈 Analytics")

if "user" not in st.session_state:
    st.warning("Login first")
    st.stop()

user = st.session_state.user

sessions = pd.read_sql(f"SELECT * FROM sessions WHERE username='{user}'", conn)

if not sessions.empty:
    sessions["date"] = pd.to_datetime(sessions["date"])
    daily = sessions.groupby("date").sum()

    st.line_chart(daily)
else:
    st.info("No data yet")