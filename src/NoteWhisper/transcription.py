import speech_recognition as sr

def transcribe_audio(audio_path: str, language: str = "en-US") -> str:
    """Transcribe audio to text"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language=language)
