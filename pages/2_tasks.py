import streamlit as st
import pandas as pd
from utils.db import conn, c
from utils.ai import generate_study_plan
from datetime import datetime, timedelta

st.title("📋 Task Manager")

if "user" not in st.session_state:
    st.warning("Login first")
    st.stop()

user = st.session_state.user

# --- Add Task ---
with st.form("add_task"):
    task = st.text_input("Task")
    deadline = st.date_input("Deadline")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    submitted = st.form_submit_button("Add Task")

    if submitted:
        c.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?)",
                  (user, task, str(deadline), priority, 0))
        conn.commit()
        st.success("Task added!")

# --- AI STUDY PLANNER ---
st.markdown("---")
st.subheader("🧠 AI Study Planner")

plan_task = st.text_input("Enter Task for Planning")
plan_deadline = st.date_input("Deadline for Plan")

if st.button("Generate Plan"):
    if plan_task:
        with st.spinner("Generating plan..."):
            tasks_list = generate_study_plan(plan_task, str(plan_deadline))
            st.session_state["plan_tasks"] = tasks_list
    else:
        st.warning("Enter a task")

# --- Show AI Plan ---
if "plan_tasks" in st.session_state:
    st.success("Here’s your plan:")

    for t in st.session_state["plan_tasks"]:
        st.write("•", t)

    # 🔥 ADD BUTTON (IMPORTANT)
    if st.button("⚡ Add Plan as Tasks"):

        today = datetime.today().date()
        deadline_date = datetime.strptime(str(plan_deadline), "%Y-%m-%d").date()
        total_days = (deadline_date - today).days + 1

        tasks_list = st.session_state["plan_tasks"]

        for i, t in enumerate(tasks_list):

            # 🎯 Detect priority
            if "Hard" in t:
                priority = "High"
            elif "Medium" in t:
                priority = "Medium"
            else:
                priority = "Low"

            # 🧹 Clean text
            clean_task = t.split(":")[-1].strip()

            # 📅 Smart scheduling
            task_date = today + timedelta(days=i % max(total_days, 1))

            c.execute(
                "INSERT INTO tasks VALUES (?, ?, ?, ?, ?)",
                (user, clean_task, str(task_date), priority, 0)
            )

        conn.commit()
        st.success("📅 Smart plan added with daily schedule!")
        st.rerun()

# --- Show Tasks ---
tasks = pd.read_sql(
    "SELECT rowid, * FROM tasks WHERE username=?",
    conn,
    params=(user,)
)

st.subheader("Your Tasks")

for _, row in tasks.iterrows():
    col1, col2, col3 = st.columns([4, 2, 1])

    # 🔥 Show priority nicely
    col1.write(f"{row['task']} 🔥{row['priority']}")
    col2.write(f"Due: {row['deadline']}")

    if col3.button("✔️", key=row["rowid"]):
        c.execute("UPDATE tasks SET done=1 WHERE rowid=?", (row["rowid"],))
        conn.commit()
        st.rerun()