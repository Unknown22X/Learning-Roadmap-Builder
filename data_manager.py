import json
from config import DATA_FILE, DEFAULT_CATEGORIES

def load_data():
    try: 
        with open(DATA_FILE, "r") as f: 
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "categories": DEFAULT_CATEGORIES.copy(),
            "roadmaps": []
        }
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_stats(data):
    """Calculate and return user statistics"""
    total_roadmaps = len(data["roadmaps"])
    total_steps = sum(len(roadmap["steps"]) for roadmap in data["roadmaps"])
    completed_steps = sum(sum(1 for step in roadmap["steps"] if step["done"]) 
                         for roadmap in data["roadmaps"])
    completion_rate = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
    return {
        "roadmaps": total_roadmaps,
        "steps": total_steps,
        "completed": completed_steps,
        "completion_rate": completion_rate
    }