# src/NoteWhisper/exceptions.py

class InvalidURLException(Exception):
    """
    Custom exception raised when a provided URL is not valid.
    """

    def __init__(self, message: str = "URL is not valid"):
        self.message = message
        super().__init__(self.message)
