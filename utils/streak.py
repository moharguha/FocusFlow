import datetime
from utils.db import conn, c
import streamlit as st  # type: ignore
def update_streak(username):
    today = datetime.date.today()

    c.execute("SELECT * FROM streaks WHERE username=?", (username,))
    data = c.fetchone()

    if data:
        last_date = datetime.date.fromisoformat(data[1])
        streak = data[2]

        if today == last_date:
            return streak

        elif today == last_date + datetime.timedelta(days=1):
            streak += 1

        else:
            streak = 1

        c.execute("UPDATE streaks SET last_date=?, streak=? WHERE username=?",
                  (str(today), streak, username))
    else:
        streak = 1
        c.execute("INSERT INTO streaks VALUES (?, ?, ?)",
                  (username, str(today), streak))

    conn.commit()
    return streak
from datetime import date

def update_streak():

    today = str(date.today())

    # initialize if not present
    if "last_completed_date" not in st.session_state:
        st.session_state.last_completed_date = None
        st.session_state.streak = 0

    last_date = st.session_state.last_completed_date

    if last_date == today:
        return  # already counted today

    # first completion OR next day
    if last_date is None:
        st.session_state.streak = 1

    else:
        from datetime import datetime, timedelta

        last = datetime.strptime(last_date, "%Y-%m-%d").date()
        current = datetime.strptime(today, "%Y-%m-%d").date()

        if current - last == timedelta(days=1):
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1

    st.session_state.last_completed_date = today