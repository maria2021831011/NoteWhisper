"""
CLI entry point for the NoteWhisper package
Usage: python -m NoteWhisper record lecture.mp3 --subject "Physics"
"""

import click


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli()
