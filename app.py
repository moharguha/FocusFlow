import streamlit as st  # type: ignore
from utils.db import init_db, c
from utils.auth import login, signup
from utils.tasks import (
    save_tasks,
    get_today_tasks,
    mark_task_done,
    get_today_stats
)
from utils.scheduler import smart_schedule
from utils.streak import update_streak
from utils.ai_feedback import generate_feedback

# 🌱 Growth visual function
def get_growth_stage(streak):
    if streak >= 8:
        return "🌸 Blossom"
    elif streak >= 5:
        return "🌳 Tree"
    elif streak >= 3:
        return "🌿 Plant"
    else:
        return "🌱 Seed"

# ✅ MUST BE FIRST
st.set_page_config(page_title="FocusFlow")

# 🎨 UI Styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #e4ecff);
}
.block-container {
    padding: 2rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
}
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg, #6c63ff, #9d8df1);
    color: white;
    font-weight: 600;
    border: none;
}
.stCheckbox {
    padding: 6px 0px;
}
.stAlert {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# --- INIT DB ---
init_db()

# --- NOT LOGGED IN ---
if "user" not in st.session_state:
    choice = st.sidebar.selectbox("Login / Signup", ["Login", "Signup"])

    if choice == "Login":
        login()
    else:
        signup()

# --- LOGGED IN ---
else:
    user = st.session_state.user

    st.title("📋 Task Manager")

    # =========================
    # 🎯 SIDEBAR
    # =========================
    st.sidebar.success(f"Welcome {user}")
    st.sidebar.write("Plan: Free" if not st.session_state.get("premium") else "Plan: Premium 💎")

    # 💎 Premium
    if st.session_state.get("premium", 0) == 0:
        if st.sidebar.button("💎 Upgrade to Premium"):
            st.session_state.premium = 1
            st.success("You are now Premium!")
    else:
        st.sidebar.info("💎 Premium User")

    # 🚪 Logout
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # =========================
    # 🔥 STREAK (DB BASED)
    # =========================
    c.execute("SELECT streak FROM streaks WHERE username=?", (user,))
    data = c.fetchone()
    streak = data[0] if data else 0

    stage = get_growth_stage(streak)

    st.sidebar.markdown("### 🌱 Your Growth")

    st.sidebar.markdown(f"""
    <div style="
        padding:15px;
        border-radius:15px;
        background:linear-gradient(135deg,#ffffff,#eef2ff);
        text-align:center;
    ">
        <h2>{stage}</h2>
        <p>🔥 {streak} day streak</p>
    </div>
    """, unsafe_allow_html=True)

    if streak >= 5:
        st.sidebar.success("You're on fire! 🔥")
    elif streak >= 3:
        st.sidebar.info("Nice consistency 👀")

    # =========================
    # 🎯 TODAY VIEW
    # =========================
    st.header("🎯 Today's Plan")

    tasks = get_today_tasks(user)

    if tasks:
        for task_id, title, priority, status in tasks:

            if status == "completed":
                st.write(f"✅ {title} ({priority})")

            else:
                if st.checkbox(f"{title} ({priority})", key=f"today_{task_id}"):

                    mark_task_done(task_id)

                    total, completed = get_today_stats(user)

                    update_streak(user, completed)

                    st.rerun()
    else:
        st.info("No tasks for today — plan something ✨")

    # =========================
    # 🧠 DAILY FEEDBACK
    # =========================
    st.divider()
    st.subheader("🧠 Daily Feedback")

    total, completed = get_today_stats(user)
    feedback = generate_feedback(total, completed)

    st.info(feedback)
    st.caption(f"📊 Completed {completed} out of {total} tasks")
    st.caption("Focus on these to win your day ⚡")

    # 📊 Progress bar
    progress = completed / total if total else 0
    st.progress(progress)

    # 🎉 Reward moment
    if total > 0 and completed == total:
        st.success("🎉 You completed everything today!")
        st.balloons()

    # =========================
    # 🤖 AI PLANNER
    # =========================
    st.divider()
    st.subheader("🧠 AI Planner / Task Generator")

    if "generated_tasks" in st.session_state:
        st.subheader("📌 Generated Tasks")

        for t in st.session_state.generated_tasks:
            st.write(f"- {t['title']} ({t['priority']})")

        if st.button("➕ Add to Planner"):
            scheduled = smart_schedule(st.session_state.generated_tasks)
            save_tasks(user, scheduled)

            st.success("✨ Tasks scheduled successfully!")

            for date, tlist in scheduled.items():
                st.subheader(f"📅 {date}")
                for t in tlist:
                    st.write(f"• {t['title']} ({t['priority']})")

            st.caption("⚖️ Balanced workload created")
            st.caption("🔥 High-priority tasks placed earlier")
        else:
            st.info("Use the AI Planner on the sidebar to generate tasks based on your goals.") 