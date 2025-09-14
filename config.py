# Configuration settings for the application
DEFAULT_CATEGORIES = ["Programming", "Design", "Languages", "Business", "Other"]
DATA_FILE = "data.json"

# UI Settings
PROGRESS_BAR_WIDTH = 30
ANIMATION_DELAY = 0.3

# Motivational messages
MOTIVATIONAL_TIPS = [
    "💡 Break large goals into smaller, manageable steps!",
    "🎯 Consistency beats perfection every time!",
    "🌟 Every expert was once a beginner!",
    "🚀 Progress, not perfection, is the goal!",
    "💪 Small daily improvements lead to stunning results!",
    "⭐ Your only competition is who you were yesterday!",
    "🎨 Learning is a journey, not a destination!",
    "🔥 The best time to start was yesterday, the second best time is now!",
]

# Add these constants
PRIORITY_COLORS = {
    "high": "red",
    "medium": "yellow", 
    "low": "green",
    "none": "dim"
}

PRIORITY_EMOJIS = {
    "high": "🚨",
    "medium": "⚠️",
    "low": "💚", 
    "none": "📝"
}

PRIORITY_ORDER = {
    "high": 0,    # Highest priority (comes first)
    "medium": 1,
    "low": 2, 
    "none": 3     # Lowest priority (comes last)
}