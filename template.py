import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s]: %(message)s"
)

# Step 1: Get project name
while True:
    project_name = input("Enter your project name (e.g., NoteWhisper): ").strip()
    if project_name:
        break
    else:
        logging.info("Project name cannot be empty. Please try again.")

logging.info(f"Creating project: {project_name}")

# Step 2: Define project files for a voice-notes package
list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/cli.py",
    f"src/{project_name}/transcription.py",
    f"src/{project_name}/keypoints.py",
    f"src/{project_name}/summarization.py",
    f"src/{project_name}/quiz.py",
    "tests/__init__.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",
    "requirements.txt",
    "requirements_dev.txt",
    "setup.py",
    "pyproject.toml",
    "setup.cfg",
    "tox.ini",
    "README.md"
]

# Step 3: Create directories and empty files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Create directories if they don't exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    # Create empty files if not present
    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w", encoding="utf-8") as fp:
            # Add basic README.md content
            if filename == "README.md":
                fp.write(f"# {project_name}\n\n")
                fp.write(f"**{project_name}** is a Python package to convert lecture audio into notes.\n")
                fp.write("- Voice-to-text (Bangla/English)\n")
                fp.write("- Keypoint extraction\n")
                fp.write("- Summary generation\n")
                fp.write("- Quiz generation\n")
                fp.write("\n## Installation\n")
                fp.write("```bash\npip install {project_name}\n```\n")
            # Add basic __init__.py comment
            elif filename == "__init__.py":
                fp.write(f"# {project_name} package init\n")
            # Add placeholder for CLI
            elif filename == "cli.py":
                fp.write(
                    '"""\nCLI entry point for the package\nUsage: python -m {project_name} record lecture.mp3 --subject "Physics"\n"""\n\n'
                    "import click\n\n@click.group()\ndef cli():\n    pass\n\nif __name__ == '__main__':\n    cli()\n"
                )
        logging.info(f"Creating a new file: {filename} at path: {filepath}")
    else:
        logging.info(f"File already exists at: {filepath}")

logging.info(f"Project {project_name} scaffolding created successfully!")
