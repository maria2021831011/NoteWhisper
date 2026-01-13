class Summarizer:
    def summarize(self, text: str) -> str:
        """Dummy summary"""
        lines = text.split(".")
        return ". ".join(lines[:3]) + "..."
