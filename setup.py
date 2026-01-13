from setuptools import setup, find_packages

setup(
    name="NoteWhisper",
    version="0.0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
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
)
