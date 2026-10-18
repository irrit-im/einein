class Something:
    def __init__(self, mood: str = "joyful") -> None:
        self.mood = mood

    def change_mood(self, new_mood: str = "devastated") -> None:
        self.mood = new_mood

    def __repr__(self) -> str:
        return self.mood + "  :D"
