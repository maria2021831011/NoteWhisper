class KeypointExtractor:
    """
    Extracts key points from lecture text.
    """
    def __init__(self, text: str):
        self.text = text

    def extract(self) -> list[str]:
        # placeholder logic
        return self.text.split(".")  # simple split as example
