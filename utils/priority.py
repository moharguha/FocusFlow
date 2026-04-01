def map_priority(level: str) -> str:
    mapping = {
        "Easy": "Low",
        "Medium": "Medium",
        "Hard": "High"
    }
    return mapping.get(level, "Medium")