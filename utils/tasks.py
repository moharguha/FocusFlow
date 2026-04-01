from utils.db import conn, c

def save_tasks(user, scheduled_tasks):
    """
    scheduled_tasks = {
        date: [ {title, priority}, ... ]
    }
    """

    for date, tasks in scheduled_tasks.items():
        for task in tasks:
            c.execute("""
                INSERT INTO tasks (user, title, priority, scheduled_date, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user,
                task["title"],
                task["priority"],
                str(date),
                "pending"
            ))

    conn.commit()
from datetime import date
from utils.db import c

def get_today_tasks(user):
    today = str(date.today())

    c.execute("""
        SELECT id, title, priority, status
        FROM tasks
        WHERE user=? AND scheduled_date=?
    """, (user, today))

    return c.fetchall()
from utils.db import conn, c

def mark_task_done(task_id):
    c.execute("""
        UPDATE tasks
        SET status='completed'
        WHERE id=?
    """, (task_id,))
    
    conn.commit()
from datetime import date
from utils.db import c

def get_today_stats(user):
    today = str(date.today())

    c.execute("""
        SELECT status FROM tasks
        WHERE user=? AND scheduled_date=?
    """, (user, today))

    results = c.fetchall()

    total = len(results)
    completed = sum(1 for r in results if r[0] == "completed")

    return total, completed