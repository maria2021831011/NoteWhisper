import click
from .transcription import transcribe_audio
from .keypoints import KeypointExtractor
from .summarization import Summarizer
from .quiz import QuizGenerator

@click.group()
def cli():
    """NoteWhisper CLI"""
    pass

@cli.command()
@click.argument("audio_file")
@click.option("--subject", default="", help="Subject of the lecture")
@click.option("--language", default="en-US", help="Language code: 'en-US' or 'bn-BD'")
def record(audio_file, subject, language):
    """Process lecture audio to notes"""
    text = transcribe_audio(audio_file, language=language)
    keypoints = KeypointExtractor().extract(text)
    summary = Summarizer().summarize(text)
    questions = QuizGenerator().generate(text)

    click.echo("=== Keypoints ===")
    click.echo("\n".join(keypoints))
    click.echo("\n=== Summary ===")
    click.echo(summary)
    click.echo("\n=== Quiz Questions ===")
    for q in questions:
        click.echo(f"- {q}")

if __name__ == "__main__":
    cli()
