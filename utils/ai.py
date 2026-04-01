# utils/ai.py

from openai import OpenAI  # type: ignore
import os

# Initialize client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------------
# 🔹 SUMMARIZE FUNCTION
# -------------------------------
def summarize(text: str) -> str:
    """
    Summarizes input text into concise bullet points.
    """

    if not text or not text.strip():
        return "⚠️ Please provide valid text."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the text into short, clear bullet points for students."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"


# -------------------------------
# 🔹 STUDY PLAN GENERATOR
# -------------------------------
def generate_study_plan(task: str, deadline: str):
    """
    Generates a structured study plan.
    Returns a list of lines.
    """

    prompt = f"""
Create a day-by-day study plan.

Task: {task}
Deadline: {deadline}

Format strictly like:
Day 1 - Easy: ...
Day 2 - Medium: ...
Day 3 - Hard: ...

Only use Easy, Medium, Hard labels.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        plan = response.choices[0].message.content.strip()

        # Clean + split into lines
        lines = [line.strip() for line in plan.split("\n") if line.strip()]

        return lines

    except Exception as e:
        return [f"❌ Error: {str(e)}"]
    

def summary_to_tasks(summary: str):
    prompt = f"""
Convert the following summary into actionable study tasks.

Rules:
- Keep tasks short
- Use bullet points
- Make them specific and practical

Summary:
{summary}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        tasks = response.choices[0].message.content.strip()

        return [t.strip("- ").strip() for t in tasks.split("\n") if t.strip()]

    except Exception as e:
        return [f"Error: {str(e)}"] 