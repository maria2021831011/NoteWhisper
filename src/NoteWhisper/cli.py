"""
CLI entry point for the package
Usage: python -m {project_name} record lecture.mp3 --subject "Physics"
"""

import click

@click.group()
def cli():
    pass

if __name__ == '__main__':
    cli()
