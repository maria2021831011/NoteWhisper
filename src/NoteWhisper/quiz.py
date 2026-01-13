class QuizGenerator:
    def generate(self, text: str) -> list[str]:
        """Dummy quiz questions"""
        return [f"What is the meaning of: {line.strip()}?" for line in text.split(".") if line.strip()][:3]
