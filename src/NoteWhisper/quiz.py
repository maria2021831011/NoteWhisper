class QuizGenerator:
    """
    Generates quiz questions from lecture text.
    """
    def __init__(self, text: str):
        self.text = text

    def generate(self) -> list[str]:
        # placeholder logic
        return [f"What is: {sentence}?" for sentence in self.text.split(".") if sentence]
