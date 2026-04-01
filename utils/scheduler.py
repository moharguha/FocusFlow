from datetime import datetime, timedelta

MAX_TASKS_PER_DAY = 5

def smart_schedule(tasks):
    """
    tasks = [
        {"title": "...", "priority": "High"},
    ]
    """

    priority_order = {"High": 1, "Medium": 2, "Low": 3}

    # Sort by priority
    tasks = sorted(tasks, key=lambda x: priority_order[x["priority"]])

    schedule = {}

    for task in tasks:
        day_offset = 0

        while True:
            date = (datetime.today() + timedelta(days=day_offset)).date()

            if date not in schedule:
                schedule[date] = []

            if len(schedule[date]) < MAX_TASKS_PER_DAY:
                schedule[date].append(task)
                break
            else:
                day_offset += 1

    return schedule