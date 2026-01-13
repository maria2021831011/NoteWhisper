"""
CLI interface for NoteWhisper
"""

import click
import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from .transcribe import Transcriber
from .keypoints import KeypointExtractor
from .summarize import Summarizer
from .quiz import QuizGenerator
from .utils import AudioProcessor, FileHandler, NoteFormatter, ConfigManager

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

def print_banner():
    """Print NoteWhisper banner"""
    banner = """
    ╔══════════════════════════════════════════╗
    ║         🎤 NoteWhisper v0.1.0            ║
    ║   Convert Lectures to Structured Notes   ║
    ╚══════════════════════════════════════════╝
    """
    click.echo(banner)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(package_name="NoteWhisper")
def cli():
    """NoteWhisper - Convert lecture audio to structured notes"""
    print_banner()

@cli.command()
@click.argument("input_source", type=click.Path(exists=False))
@click.option(
    "--subject",
    "-s",
    default="General",
    help="Subject name (e.g., Physics, Mathematics)",
    show_default=True,
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["bn", "en", "auto"]),
    default="auto",
    help="Language: bn (Bangla), en (English), auto (detect)",
    show_default=True,
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file/directory path",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["markdown", "html", "txt", "pdf", "docx"]),
    default="markdown",
    help="Output format",
    show_default=True,
)
@click.option(
    "--detail",
    "-d",
    type=click.Choice(["minimal", "standard", "detailed"]),
    default="standard",
    help="Level of detail in notes",
    show_default=True,
)
@click.option(
    "--model",
    "-m",
    default="base",
    help="Whisper model size (tiny, base, small, medium, large)",
    show_default=True,
)
@click.option(
    "--youtube",
    "-y",
    is_flag=True,
    help="Input is a YouTube URL",
)
@click.option(
    "--keep-audio",
    is_flag=True,
    help="Keep processed audio files",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Quiet mode - minimal output",
)
def process(
    input_source: str,
    subject: str,
    language: str,
    output: Optional[str],
    format: str,
    detail: str,
    model: str,
    youtube: bool,
    keep_audio: bool,
    quiet: bool,
):
    """Process audio/video file or YouTube URL"""
    
    if not quiet:
        click.echo("🎤 NoteWhisper - Processing Started")
        click.echo(f"📁 Input: {input_source}")
        click.echo(f"📚 Subject: {subject}")
    
    start_time = datetime.now()
    
    try:
        # Initialize components
        config = ConfigManager()
        audio_processor = AudioProcessor()
        file_handler = FileHandler()
        transcriber = Transcriber(model_size=model)
        keypoint_extractor = KeypointExtractor(subject=subject)
        summarizer = Summarizer()
        quiz_generator = QuizGenerator()
        note_formatter = NoteFormatter(format=format)
        
        # Handle YouTube URL
        if youtube:
            if not quiet:
                click.echo("🌐 Downloading from YouTube...")
            input_source = audio_processor.download_youtube_audio(input_source)
        
        # Check if input exists
        if not Path(input_source).exists():
            raise FileNotFoundError(f"Input file not found: {input_source}")
        
        # Process audio
        if not quiet:
            click.echo("🔊 Processing audio file...")
        audio_path = audio_processor.preprocess_audio(input_source)
        
        # Transcribe
        if not quiet:
            click.echo("📝 Transcribing...")
        transcript = transcriber.transcribe(
            audio_path=audio_path,
            language=language,
        )
        
        if not transcript or len(transcript.strip()) < 10:
            raise ValueError("Transcription failed or too short")
        
        # Extract keypoints
        if not quiet:
            click.echo("🎯 Extracting key points...")
        keypoints = keypoint_extractor.extract(transcript)
        
        # Generate summary
        if not quiet:
            click.echo("📊 Generating summary...")
        summary = summarizer.summarize(transcript, detail_level=detail)
        
        # Generate quiz
        if not quiet:
            click.echo("❓ Generating quiz questions...")
        quiz_questions = quiz_generator.generate(transcript, num_questions=5)
        
        # Format notes
        if not quiet:
            click.echo("📄 Formatting notes...")
        formatted_notes = note_formatter.format(
            transcript=transcript,
            keypoints=keypoints,
            summary=summary,
            quiz_questions=quiz_questions,
            subject=subject,
            source=input_source,
        )
        
        # Save output
        if not output:
            output = file_handler.generate_output_path(
                input_source=input_source,
                subject=subject,
                format=format,
            )
        
        file_handler.save_output(
            content=formatted_notes,
            output_path=output,
            format=format,
        )
        
        # Cleanup
        if not keep_audio:
            audio_processor.cleanup(audio_path)
            if youtube and Path(input_source).exists():
                Path(input_source).unlink()
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        if not quiet:
            click.echo(f"✅ Success! Notes saved to: {output}")
            click.echo(f"⏱️  Processing time: {processing_time:.2f} seconds")
            click.echo(f"📝 Transcript length: {len(transcript)} characters")
            click.echo(f"🎯 Key points: {len(keypoints)}")
            click.echo(f"❓ Quiz questions: {len(quiz_questions)}")
        
        # Show preview
        if not quiet and click.confirm("Show preview?"):
            preview = formatted_notes[:500] + "..." if len(formatted_notes) > 500 else formatted_notes
            click.echo(f"\n📋 Preview:\n{preview}\n")
        
        return {
            "status": "success",
            "output_path": output,
            "transcript_length": len(transcript),
            "keypoints_count": len(keypoints),
            "quiz_questions_count": len(quiz_questions),
            "processing_time": processing_time,
        }
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        if not quiet:
            click.echo(f"❌ Error: {e}", err=True)
        return {"status": "error", "message": str(e)}

@cli.command()
@click.option(
    "--duration",
    "-d",
    type=int,
    default=300,
    help="Recording duration in seconds",
    show_default=True,
)
@click.option(
    "--subject",
    "-s",
    default="Recording",
    help="Subject name",
    show_default=True,
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output audio file path",
)
@click.option(
    "--process",
    "-p",
    is_flag=True,
    help="Process recording immediately",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Quiet mode - minimal output",
)
def record(duration: int, subject: str, output: Optional[str], process: bool, quiet: bool):
    """Record audio from microphone"""
    
    if not quiet:
        click.echo("🎤 Recording from microphone...")
    
    try:
        audio_processor = AudioProcessor()
        
        if not output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = f"NoteWhisper_Recording_{subject}_{timestamp}.wav"
        
        if not quiet:
            click.echo(f"⏱️  Recording for {duration} seconds...")
            click.echo("🎙️  Speak now...")
            click.echo("🛑 Press Ctrl+C to stop early")
        
        audio_path = audio_processor.record_audio(
            duration=duration,
            output_path=output,
        )
        
        if not quiet:
            click.echo(f"✅ Recording saved: {audio_path}")
        
        if process:
            ctx = click.get_current_context()
            ctx.invoke(
                process,
                input_source=audio_path,
                subject=subject,
                language="auto",
                output=None,
                format="markdown",
                detail="standard",
                model="base",
                youtube=False,
                keep_audio=True,
                quiet=quiet,
            )
        
        return {"status": "success", "audio_path": audio_path}
        
    except KeyboardInterrupt:
        if not quiet:
            click.echo("\n⏹️ Recording stopped by user")
        return {"status": "interrupted"}
    except ImportError:
        if not quiet:
            click.echo("❌ PyAudio not installed. Install with:")
            click.echo("   pip install pyaudio")
            click.echo("   On Linux: sudo apt-get install portaudio19-dev")
        return {"status": "error", "message": "PyAudio not installed"}
    except Exception as e:
        logger.error(f"Recording failed: {e}")
        if not quiet:
            click.echo(f"❌ Error: {e}", err=True)
        return {"status": "error", "message": str(e)}

@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option(
    "--subject",
    "-s",
    required=True,
    help="Subject name for all files",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    help="Output directory",
)
@click.option(
    "--pattern",
    "-p",
    default="*.mp3,*.wav,*.m4a,*.flac",
    help="File pattern to match",
    show_default=True,
)
@click.option(
    "--parallel",
    is_flag=True,
    help="Process files in parallel (experimental)",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Quiet mode - minimal output",
)
def batch(
    directory: str,
    subject: str,
    output_dir: Optional[str],
    pattern: str,
    parallel: bool,
    quiet: bool,
):
    """Process multiple audio files in a directory"""
    
    if not quiet:
        click.echo(f"📁 Batch processing directory: {directory}")
    
    try:
        file_handler = FileHandler()
        patterns = [p.strip() for p in pattern.split(",")]
        audio_files = file_handler.find_audio_files(directory, patterns)
        
        if not audio_files:
            if not quiet:
                click.echo("❌ No audio files found")
            return {"status": "error", "message": "No audio files found"}
        
        if not quiet:
            click.echo(f"📊 Found {len(audio_files)} audio files")
        
        results = []
        for i, audio_file in enumerate(audio_files, 1):
            if not quiet:
                click.echo(f"\n[{i}/{len(audio_files)}] Processing: {audio_file.name}")
            
            ctx = click.get_current_context()
            result = ctx.invoke(
                process,
                input_source=str(audio_file),
                subject=subject,
                language="auto",
                output=output_dir,
                format="markdown",
                detail="standard",
                model="base",
                youtube=False,
                keep_audio=False,
                quiet=quiet,
            )
            
            results.append(result)
        
        if not quiet:
            click.echo(f"\n✅ Batch processing completed!")
            successful = sum(1 for r in results if r.get("status") == "success")
            click.echo(f"📈 Successful: {successful}/{len(audio_files)}")
        
        return {
            "status": "success",
            "total_files": len(audio_files),
            "successful": sum(1 for r in results if r.get("status") == "success"),
            "failed": sum(1 for r in results if r.get("status") == "error"),
            "results": results,
        }
        
    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        if not quiet:
            click.echo(f"❌ Error: {e}", err=True)
        return {"status": "error", "message": str(e)}

@cli.command()
@click.option(
    "--show",
    is_flag=True,
    help="Show current configuration",
)
@click.option(
    "--reset",
    is_flag=True,
    help="Reset to default configuration",
)
@click.option(
    "--key",
    "-k",
    help="Configuration key to get/set",
)
@click.option(
    "--value",
    "-v",
    help="Value to set for the key",
)
def config(show: bool, reset: bool, key: Optional[str], value: Optional[str]):
    """Manage configuration"""
    
    config_manager = ConfigManager()
    
    if reset:
        config_manager.reset()
        click.echo("✅ Configuration reset to defaults")
        return
    
    if show:
        current_config = config_manager.load()
        click.echo("⚙️  Current Configuration:")
        for k, v in current_config.items():
            click.echo(f"  {k}: {v}")
        return
    
    if key and value:
        config_manager.set(key, value)
        click.echo(f"✅ Configuration updated: {key} = {value}")
    elif key:
        val = config_manager.get(key)
        click.echo(f"{key}: {val}")
    else:
        click.echo("❌ Please specify --key or use --show")

@cli.command()
def sample():
    """Download and process sample audio"""
    from .utils import download_sample_audio
    
    click.echo("📥 Downloading sample audio...")
    sample_path = download_sample_audio()
    
    if sample_path:
        click.echo(f"✅ Sample downloaded: {sample_path}")
        
        # Process the sample
        ctx = click.get_current_context()
        ctx.invoke(
            process,
            input_source=sample_path,
            subject="Physics",
            language="bn",
            output="sample_notes.md",
            format="markdown",
            detail="detailed",
            model="base",
            youtube=False,
            keep_audio=True,
            quiet=False,
        )

@cli.command()
def demo():
    """Run a demo with sample audio"""
    click.echo("🚀 Starting NoteWhisper Demo...")
    
    # First, try to download sample
    ctx = click.get_current_context()
    ctx.invoke(sample)
    
    click.echo("\n" + "="*50)
    click.echo("💡 Try these commands:")
    click.echo("  notewhisper process audio.mp3 --subject Physics")
    click.echo("  notewhisper record --duration 60 --subject Math")
    click.echo("  notewhisper batch ./lectures/ --subject Biology")
    click.echo("="*50)

def main():
    """Entry point for console scripts"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"CLI error: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()