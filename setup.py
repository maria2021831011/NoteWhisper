import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.1"

REPO_NAME = "NoteWhisper"
AUTHOR_USER_NAME = "maria2021831011"  
AUTHOR_EMAIL = "ritukhan534@gmail.com"    
SRC_REPO = "NoteWhisper"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package to convert lecture audio into notes (Bangla/English)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
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
            "tox>=3.25.1",
            "flake8>=6.1.0",
            "mypy>=1.5.1",
            "black>=24.3.0",
            "isort>=6.0.0",
            "pre-commit>=3.4.0",
            "mkdocs-material",
        ]
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "note-whisper=NoteWhisper.cli:cli",  # CLI command
        ],
    },
)
