import os
import re
import sys
from pathlib import Path

import yt_dlp


def find_ffmpeg_dir():
    """Find a FFmpeg directory containing both ffmpeg and ffprobe."""
    candidates = []

    for path_entry in os.environ.get("PATH", "").split(os.pathsep):
        if path_entry:
            path = Path(path_entry).expanduser()
            if path.exists():
                candidates.append(path)

    try:
        import imageio_ffmpeg
        exe_path = Path(imageio_ffmpeg.get_ffmpeg_exe()).expanduser()
        if exe_path.exists():
            candidates.append(exe_path.parent)
    except Exception:
        pass

    seen = set()
    for candidate in candidates:
        resolved = str(candidate.resolve()) if candidate.exists() else str(candidate)
        if resolved in seen:
            continue
        seen.add(resolved)

        ffmpeg = candidate / "ffmpeg.exe" if os.name == "nt" else candidate / "ffmpeg"
        ffprobe = candidate / "ffprobe.exe" if os.name == "nt" else candidate / "ffprobe"
        if ffmpeg.exists() and ffprobe.exists():
            return str(candidate)

    return None


def ensure_ffmpeg_available():
    """Exit early with a clear message if FFmpeg is missing."""
    ffmpeg_dir = find_ffmpeg_dir()
    if ffmpeg_dir:
        return ffmpeg_dir

    print("\nFFmpeg is missing or incomplete.")
    print("yt-dlp needs both ffmpeg.exe and ffprobe.exe to convert audio.")
    print("Windows quick fix: winget install Gyan.Dev.FFmpeg")
    print("Then restart this script.")
    raise SystemExit(1)


def sanitize_filename(name):
    """Remove characters that are not safe for Windows file names."""
    return re.sub(r'[\\/:*?"<>|]', "", name).strip() or "youtube_music"


def select_save_directory():
    """Ask for output folder; default to a Music/YoutubeMusic folder in the user's home directory."""
    default_dir = Path.home() / "Music" / "YoutubeMusic"
    print("\n--- Save Location ---")
    user_input = input(f"Enter folder path to save songs [Default: {default_dir}]: ").strip()
    target_dir = Path(user_input).expanduser() if user_input else default_dir
    target_dir = target_dir.resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    return str(target_dir)


def select_format():
    """Choose audio format."""
    print("\n--- Audio Format ---")
    print("1. MP3 [Recommended]")
    print("2. M4A")
    print("3. WAV")
    choice = input("Enter choice (1-3) [Default: 1]: ").strip()

    format_map = {"1": "mp3", "2": "m4a", "3": "wav"}
    return format_map.get(choice, "mp3")


def select_quality():
    """Choose quality for the extracted audio."""
    print("\n--- Audio Quality ---")
    print("1. Best available [Default]")
    print("2. 320 kbps")
    print("3. 256 kbps")
    print("4. 128 kbps")
    choice = input("Enter choice (1-4) [Default: 1]: ").strip()

    quality_map = {"1": "0", "2": "320K", "3": "256K", "4": "128K"}
    return quality_map.get(choice, "0")


def build_ytdlp_options(output_dir, audio_format, quality):
    """Create yt-dlp options for downloading and converting audio."""
    base_path = Path(output_dir)
    output_template = str(base_path / "%(title)s.%(ext)s")
    ffmpeg_dir = ensure_ffmpeg_available()

    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": False,
        "quiet": False,
        "no_warnings": True,
        "extract_flat": False,
        "postprocessors": [],
        "paths": {"home": str(base_path)},
        "ffmpeg_location": ffmpeg_dir,
        "ignoreerrors": True,
        "extractor_retries": 10,
        "retries": 10,
        "fragment_retries": 10,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        },
        "extractor_args": {
            "youtube": ["player_client=android", "player_client=web", "player_skip=webpage"]
        },
    }

    if audio_format == "mp3":
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality,
        }]
    elif audio_format == "m4a":
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": quality,
        }]
    elif audio_format == "wav":
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": quality,
        }]

    return options


def download_youtube_music(url, output_dir, audio_format, quality):
    """Download music from YouTube using yt-dlp."""
    if not url:
        raise ValueError("No URL provided.")

    options = build_ytdlp_options(output_dir, audio_format, quality)

    print(f"\nDownloading from: {url}")
    print(f"Output folder: {output_dir}")
    print(f"Format: {audio_format.upper()}")

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print("\nDownload complete.")
    except Exception as exc:
        print(f"\nDownload failed: {exc}")
        raise


def main():
    print("==================================================")
    print("         YouTube Music Downloader")
    print("==================================================")
    print("Use only for content you are authorized to download.")

    url = input("\nPaste YouTube music URL or playlist URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    output_dir = select_save_directory()
    audio_format = select_format()
    quality = select_quality()

    download_youtube_music(url, output_dir, audio_format, quality)
    print(f"\nFiles saved in: {os.path.abspath(output_dir)}")
    print("==================================================")


if __name__ == "__main__":
    main()
