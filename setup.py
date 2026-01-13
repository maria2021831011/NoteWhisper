import setuptools
from pathlib import Path

# Read the README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="NoteWhisper",                     # package name
    version="0.0.1",
    author="maria2021831011",
    author_email="ritukhan534@gmail.com",
    description="Convert lecture audio into structured notes (Bangla/English)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maria2021831011/NoteWhisper",
    packages=setuptools.find_packages(where="src"),   # find code in src/
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "SpeechRecognition>=3.8.1",
        "pydub>=0.25.1",
        "torch>=2.1.0",
        "transformers>=4.34.0",
        "openai>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.2",
            "flake8>=6.1.0",
            "mypy>=1.5.1",
            "tox>=3.25.1",
            "black>=24.3.0",
            "isort>=6.0.0",
            "pre-commit>=3.4.0",
            "mkdocs-material",
        ]
    },
    entry_points={
        "console_scripts": [
            "note-whisper=NoteWhisper.cli:cli",  # CLI command
        ],
    },
)
