import streamlit as st
import time
from datetime import datetime
from utils.db import conn, c
from utils.streak import update_streak

st.title("⏳ Focus Mode")

if "user" not in st.session_state:
    st.warning("Login first")
    st.stop()

user = st.session_state.user

minutes = st.slider("Focus Time (minutes)", 1, 60, 25)

if st.button("Start Focus"):
    placeholder = st.empty()

    for i in range(minutes * 60):
        mins, secs = divmod(minutes*60 - i, 60)
        placeholder.metric("Time Left", f"{mins:02d}:{secs:02d}")
        time.sleep(1)

    c.execute("INSERT INTO sessions VALUES (?, ?, ?)",
              (user, str(datetime.now().date()), minutes))
    conn.commit()

    st.success("Session complete 🔥")

    # 🔥 Streak update
    streak = update_streak(user)

    st.balloons()  # 🎉 confetti
    st.success(f"🔥 Streak: {streak} days!")

    # 🏆 Badges (properly indented)
    if streak == 7:
        st.success("🏆 7 Day Streak! You're on fire!")

    elif streak == 30:
        st.success("👑 30 Day Streak! Elite discipline!")

    elif streak == 100:
        st.success("💀 100 Day Streak! You are unstoppable.")