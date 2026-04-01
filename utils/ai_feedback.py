def generate_feedback(total, completed):

    # No tasks case
    if total == 0:
        return "No tasks today. Plan something and start strong tomorrow."

    completion_rate = completed / total

    # Perfect day
    if completion_rate == 1:
        return "Perfect day. You completed everything — elite consistency."

    # Good progress
    elif completion_rate >= 0.7:
        return "Strong progress. You're building solid momentum."

    # Okay but can improve
    elif completion_rate >= 0.4:
        return "Decent effort, but try focusing on high-priority tasks first."

    # Low performance
    else:
        return "Low completion today. Try reducing workload or starting earlier."