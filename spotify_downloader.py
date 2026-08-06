import subprocess
import sys
import os

def get_ffmpeg_path():
    """Locate ffmpeg executable path using imageio_ffmpeg if available."""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"

def select_save_directory():
    """Prompt user for target save directory, defaulting to user's Downloads folder."""
    default_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    print("\n--- Save Location ---")
    user_input = input(f"Enter folder path to save files [Default: {default_dir}]: ").strip()
    target_dir = user_input if user_input else default_dir
    target_dir = os.path.abspath(os.path.expanduser(target_dir))
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def select_format():
    """Prompt user for audio format."""
    print("\n--- Select Audio Format ---")
    print("1. mp3  [Default]")
    print("2. m4a")
    print("3. flac")
    print("4. wav")
    choice = input("Enter choice (1-4): ").strip()
    return {"1": "mp3", "2": "m4a", "3": "flac", "4": "wav"}.get(choice, "mp3")

def select_quality():
    """Prompt user for audio quality."""
    print("\n--- Select Audio Quality ---")
    print("1. 320k (Highest) [Default]")
    print("2. 256k (High)")
    print("3. 128k (Low)")
    print("4. auto (Original YouTube quality)")
    choice = input("Enter choice (1-4): ").strip()
    return {"1": "320k", "2": "256k", "3": "128k", "4": "auto"}.get(choice, "320k")

def select_organization():
    """Prompt user for folder organization."""
    print("\n--- Folder Organization ---")
    choice = input("Organize tracks into subfolders based on Playlist/Album name? (y/n) [Default: y]: ").strip().lower()
    return choice != "n"

def select_lyrics():
    """Prompt user to generate lyrics."""
    print("\n--- Lyrics ---")
    choice = input("Download synced lyrics (.lrc files)? (y/n) [Default: n]: ").strip().lower()
    return choice == "y"

def download_spotify_track(url: str, output_dir: str, audio_format: str, bitrate: str, organize: bool, lyrics: bool):
    """
    Downloads a Spotify track/playlist/album using spotdl.
    """
    try:
        # Check if spotdl is installed
        subprocess.run([sys.executable, "-m", "spotdl", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\nspotdl is not installed or not in PATH.")
        print("Please install it by running: pip install spotdl")
        sys.exit(1)

    print(f"\nFetching metadata and downloading {url}...")
    
    ffmpeg_path = get_ffmpeg_path()
    
    # Build spotdl command
    cmd = [
        sys.executable, "-m", "spotdl", url, 
        "--format", audio_format, 
        "--bitrate", bitrate,
        "--ffmpeg", ffmpeg_path,
        "--preload"
    ]
    
    if organize:
        # Only use {list-name} in the path if it's actually a list (album/playlist/artist)
        # Otherwise, an empty {list-name} causes the path to start with '/' which resolves to C:\ on Windows
        if any(x in url.lower() for x in ["playlist", "album", "artist"]):
            cmd.extend(["--output", "{list-name}/{artist} - {title}.{output-ext}"])
        else:
            cmd.extend(["--output", "{artist} - {title}.{output-ext}"])
        
    if lyrics:
        cmd.append("--generate-lrc")

    try:
        original_cwd = os.getcwd()
        os.chdir(output_dir)
        
        subprocess.run(cmd, check=True)
        
        os.chdir(original_cwd)
        print("\nDownload completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred during download: {e}")
        sys.exit(1)

def main():
    print("==================================================")
    print("      Music Interactive Downloader (spotDL)       ")
    print("==================================================")
    
    url = input("\nEnter Spotify / YouTube Music URL (or search query): ").strip()
    if not url:
        print("No URL provided. Exiting.")
        sys.exit(1)
        
    base_dir = select_save_directory()
    audio_format = select_format()
    bitrate = select_quality()
    organize = select_organization()
    lyrics = select_lyrics()
    
    download_spotify_track(url, base_dir, audio_format, bitrate, organize, lyrics)
    
    print("\n==================================================")
    print(f" All files saved in: {os.path.abspath(base_dir)}")
    print("==================================================")

if __name__ == "__main__":
    main()
