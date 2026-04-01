import streamlit as st
import pandas as pd
from utils.db import conn, c
from datetime import date

st.title("📊 Dashboard")

if "user" not in st.session_state:
    st.warning("Please login first")
    st.stop()

user = st.session_state.user

# --- Load Data (safer) ---
tasks = pd.read_sql("SELECT * FROM tasks WHERE user=?", conn, params=(user,))
sessions = pd.read_sql("SELECT * FROM sessions WHERE username=?", conn, params=(user,))

# --- Metrics ---
total_tasks = len(tasks)
total = len(tasks)
completed = len(tasks[tasks["status"] == "completed"])

st.metric("Total Tasks", total_tasks)
st.metric("Completed Tasks", completed)

# --- Streak ---
c.execute("SELECT streak, last_date FROM streaks WHERE username=?", (user,))
result = c.fetchone()

if result:
    streak, last_date = result
    st.metric("🔥 Current Streak", streak)

    last_date = date.fromisoformat(last_date)

    if last_date < date.today():
        st.warning("⚠️ You haven’t studied today — don’t break your streak!")
else:
    st.metric("🔥 Current Streak", 0)

# 💅 Motivation (always visible)
st.markdown("## 🔥 Stay Consistent. Stay Dangerous.")

# --- Pending Tasks ---
st.subheader("📋 Pending Tasks")
pending = tasks[tasks["done"] == 0]

if not pending.empty:
    st.write(pending[["task", "deadline", "priority"]])
else:
    st.info("No pending tasks 😌")

# --- Focus Time ---
st.subheader("⏳ Focus Summary")

if not sessions.empty:
    total_minutes = sessions["minutes"].sum()
    st.metric("Total Focus Time (mins)", int(total_minutes))
else:
    st.info("No focus sessions yet")
