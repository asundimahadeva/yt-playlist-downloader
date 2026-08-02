import os
import sys
import re
import yt_dlp
import imageio_ffmpeg

def clean_filename(name):
    """Sanitize directory or file names for Windows filesystem."""
    return re.sub(r'[\\/*?:"<>|]', '', name).strip()

def get_ffmpeg_path():
    """Locate ffmpeg executable path."""
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def format_time(seconds):
    """Format seconds into HH:MM:SS or MM:SS."""
    if seconds is None:
        return "00:00"
    seconds = int(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"

def parse_description_chapters(description):
    """Fallback parser to extract timestamped chapters from video description."""
    if not description:
        return []
    chapters = []
    pattern = re.compile(r'(?:^|\n)\s*(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\s*[-:]?\s*(.+)')
    for match in pattern.findall(description):
        h, m, s, title = match
        total_sec = (int(h) * 3600 if h else 0) + int(m) * 60 + int(s)
        clean_t = title.strip()
        if clean_t:
            chapters.append({'start_time': total_sec, 'title': clean_t})
    return chapters

def select_save_directory():
    """Prompt user for target save directory, defaulting to user's Downloads folder."""
    default_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    print("\n--- Save Location ---")
    user_input = input(f"Enter folder path to save files [Default: {default_dir}]: ").strip()
    target_dir = user_input if user_input else default_dir
    target_dir = os.path.abspath(os.path.expanduser(target_dir))
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def select_quality():
    """Prompt user to select desired video quality."""
    print("\n--- Select Video Quality ---")
    print("1. 1080p (Full HD)")
    print("2. 720p  (HD)")
    print("3. 480p  (SD)")
    print("4. 360p  (Low)")
    print("5. Best Available")
    
    choice = input("Enter choice (1-5) [Default: 1]: ").strip()
    
    quality_map = {
        "1": "bv*[height<=1080]+ba/b[height<=1080]/b",
        "2": "bv*[height<=720]+ba/b[height<=720]/b",
        "3": "bv*[height<=480]+ba/b[height<=480]/b",
        "4": "bv*[height<=360]+ba/b[height<=360]/b",
        "5": "bv*+ba/b"
    }
    return quality_map.get(choice, quality_map["1"])

def select_subtitles():
    """Prompt user whether to embed closed captions / subtitles."""
    sub_choice = input("\nEmbed English Closed Captions (Subtitles)? (y/n) [Default: y]: ").strip().lower()
    return sub_choice != "n"

def select_chapter_mode():
    """Prompt user how they want chapters/timestamps handled."""
    print("\n--- Chapter & Timestamp Options ---")
    print("1. Embed Chapters in MP4 (Clickable chapter timeline in VLC / Media Player) [Default]")
    print("2. Split Video into Separate Clips per Chapter/Timestamp")
    print("3. Regular Download (No special chapter processing)")
    
    choice = input("Enter choice (1-3) [Default: 1]: ").strip()
    return choice if choice in ["1", "2", "3"] else "1"

def generate_chapters_html(video_info_list, target_dir, folder_title):
    """Generate an interactive HTML file with clickable chapter timestamps."""
    html_path = os.path.join(target_dir, "CHAPTERS.html")
    
    cards_html = ""
    for video in video_info_list:
        v_title = video.get('title', 'Video')
        v_url = video.get('webpage_url', '#')
        chapters = video.get('chapters')
        
        if not chapters:
            chapters = parse_description_chapters(video.get('description', ''))
        
        chapter_items = ""
        if chapters:
            for ch in chapters:
                start_sec = int(ch.get('start_time', 0))
                time_str = format_time(start_sec)
                ch_title = ch.get('title', 'Chapter')
                timestamp_url = f"{v_url}&t={start_sec}s" if '?' in v_url else f"{v_url}?t={start_sec}s"
                chapter_items += f'''
                <li class="chapter-item">
                    <span class="badge">{time_str}</span>
                    <a href="{timestamp_url}" target="_blank" class="ch-link">{ch_title}</a>
                </li>'''
        else:
            chapter_items = '<li class="no-chapters">No timestamped chapters found for this video.</li>'
            
        cards_html += f'''
        <div class="card">
            <h2 class="video-title">{v_title}</h2>
            <p><a href="{v_url}" target="_blank" class="yt-link">▶ Watch on YouTube</a></p>
            <ul class="chapter-list">
                {chapter_items}
            </ul>
        </div>'''
        
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{folder_title} - Video Chapters & Timestamps</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 2rem;
        }}
        h1 {{
            color: var(--accent);
            text-align: center;
            margin-bottom: 2rem;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            border: 1px solid #334155;
        }}
        .video-title {{
            margin-top: 0;
            font-size: 1.25rem;
            color: #ffffff;
        }}
        .yt-link {{
            color: #f43f5e;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .yt-link:hover {{ text-decoration: underline; }}
        .chapter-list {{
            list-style: none;
            padding: 0;
            margin-top: 1rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 0.75rem;
        }}
        .chapter-item {{
            background: #090d16;
            padding: 0.6rem 0.8rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            border: 1px solid #1e293b;
        }}
        .badge {{
            background: #0284c7;
            color: #ffffff;
            font-weight: bold;
            font-size: 0.8rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: monospace;
        }}
        .ch-link {{
            color: var(--text);
            text-decoration: none;
            font-size: 0.9rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .ch-link:hover {{
            color: var(--accent);
            text-decoration: underline;
        }}
        .no-chapters {{
            color: var(--text-muted);
            font-style: italic;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📌 {folder_title} - Video Chapters Index</h1>
        {cards_html}
    </div>
</body>
</html>'''

    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n[Chapter Index Created] '{html_path}'")
    except Exception as e:
        print(f"Failed to write CHAPTERS.html: {e}")

def main():
    print("==================================================")
    print("      YouTube Interactive Downloader & Chapters    ")
    print("==================================================")
    
    url = input("\nEnter YouTube Video or Playlist URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        sys.exit(1)
        
    base_dir = select_save_directory()
    format_spec = select_quality()
    embed_subs = select_subtitles()
    chapter_mode = select_chapter_mode()
    
    ffmpeg_path = get_ffmpeg_path()
    
    print("\nFetching metadata & chapters...")
    
    output_folder = base_dir
    is_playlist = False
    playlist_title = "Downloaded Videos"
    video_entries = []

    ydl_opts_meta = {
        'skip_download': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts_meta) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if info:
                if ('_type' in info and info['_type'] == 'playlist') or 'entries' in info:
                    is_playlist = True
                    playlist_title = info.get('title', 'Downloaded Playlist')
                    raw_entries = info.get('entries', [])
                    for e in raw_entries:
                        if e:
                            video_entries.append(e)
                else:
                    playlist_title = info.get('title', 'Downloaded Video')
                    video_entries.append(info)
        except Exception as e:
            print(f"Warning: Metadata fetch error: {e}")

    if is_playlist:
        clean_title = clean_filename(playlist_title)
        output_folder = os.path.join(base_dir, clean_title)
        os.makedirs(output_folder, exist_ok=True)
        print(f"\n[Playlist Detected] '{playlist_title}'")
        print(f"[Folder Created] '{output_folder}'")
        output_template = os.path.join(output_folder, "%(playlist_index)s - %(title)s.%(ext)s")
    else:
        print(f"\n[Single Video Detected] '{playlist_title}'")
        output_template = os.path.join(output_folder, "%(title)s.%(ext)s")

    # Postprocessors list to ensure chapter metadata is explicitly written by FFmpeg into MP4
    postprocessors = []

    # Main YoutubeDL options
    ydl_opts = {
        'format': format_spec,
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': output_template,
        'ignoreerrors': True,
    }
    
    # Subtitles
    if embed_subs:
        ydl_opts.update({
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en.*', 'en'],
        })
        postprocessors.append({'key': 'FFmpegEmbedSubtitle'})
        
    # Chapters
    if chapter_mode == "1":
        ydl_opts['embedchapters'] = True
        postprocessors.append({'key': 'FFmpegMetadata', 'add_chapters': True})
    elif chapter_mode == "2":
        ydl_opts['splitchapters'] = True
        if is_playlist:
            ydl_opts['outtmpl'] = {
                'default': output_template,
                'chapter': os.path.join(output_folder, "%(playlist_index)s - %(title)s - %(section_number)02d - %(section_title)s.%(ext)s")
            }
        else:
            ydl_opts['outtmpl'] = {
                'default': output_template,
                'chapter': os.path.join(output_folder, "%(title)s - %(section_number)02d - %(section_title)s.%(ext)s")
            }
            
    ydl_opts['postprocessors'] = postprocessors
        
    print("\nStarting Download...\n")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    # Automatic post-download cleanup: delete non-mp4 leftover files (.vtt, .webm, etc.)
    target_dir = output_folder
    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.lower().endswith(".mp4") and not file.lower().endswith(".html"):
                filepath = os.path.join(root, file)
                try:
                    os.remove(filepath)
                except Exception:
                    pass

    # Generate CHAPTERS.html dashboard
    if video_entries:
        generate_chapters_html(video_entries, target_dir, playlist_title)

    print("\n==================================================")
    print("       Download & Processing Complete!            ")
    print(f" Saved in: {os.path.abspath(target_dir)}")
    print("==================================================")

if __name__ == "__main__":
    main()
