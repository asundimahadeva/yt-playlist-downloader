# 🎬 YouTube Playlist & Video Downloader

An interactive, feature-rich Python CLI tool powered by [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and `ffmpeg` for downloading YouTube videos and playlists in up to 1080p Full HD quality with embedded closed captions and chapter markers.

---

## ✨ Features

- 📹 **Quality Selection**: Choose your preferred video resolution (**1080p**, **720p**, **480p**, **360p**, or **Best Available**).
- 📁 **Automatic Playlist Folders**: Automatically detects playlists, creates a dedicated folder named after the playlist, and numbers the files (`01 - Title.mp4`, `02 - Title.mp4`, etc.).
- 💬 **Embedded Closed Captions (Subtitles)**: Automatically downloads and embeds English subtitles directly into the `.mp4` video container.
- 📌 **Embedded Video Chapters**: Embeds YouTube chapter markers into `.mp4` metadata for quick timeline navigation in media players like VLC, mpv, or Windows Media Player.
- 🌐 **Interactive `CHAPTERS.html` Index**: Automatically generates a dark-mode HTML dashboard inside the download folder with clickable timestamps that launch chapters directly on YouTube.
- 📂 **Custom Save Directory**: Prompt to choose your save directory, defaulting to your system's `Downloads` folder.
- 🧹 **Automatic Cleanup**: Automatically deletes temporary files (`.vtt`, `.webm`, etc.) so only clean `.mp4` video files remain.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher installed on your system.

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/yt-playlist-downloader.git
cd yt-playlist-downloader

pip install -r requirements.txt
```

---

## 📖 Usage

Run the interactive script:

```bash
python youtube_vid_downloader.py
```

### Interactive Prompts Walkthrough:

```text
==================================================
      YouTube Interactive Downloader & Chapters    
==================================================

Enter YouTube Video or Playlist URL: https://youtube.com/playlist?list=...

--- Save Location ---
Enter folder path to save files [Default: C:\Users\Abhijeet_2\Downloads]: 

--- Select Video Quality ---
1. 1080p (Full HD)
2. 720p  (HD)
3. 480p  (SD)
4. 360p  (Low)
5. Best Available
Enter choice (1-5) [Default: 1]: 1

Embed English Closed Captions (Subtitles)? (y/n) [Default: y]: y

--- Chapter & Timestamp Options ---
1. Embed Chapters in MP4 (Clickable chapter timeline in VLC / Media Player) [Default]
2. Split Video into Separate Clips per Chapter/Timestamp
3. Regular Download (No special chapter processing)
Enter choice (1-3) [Default: 1]: 1

[Playlist Detected] 'SQL Tutorial'
[Folder Created] 'C:\Users\Abhijeet_2\Downloads\SQL Tutorial'

Starting Download...
...
==================================================
       Download & Processing Complete!            
 Saved in: C:\Users\Abhijeet_2\Downloads\SQL Tutorial
==================================================
```

---

## 🛠 Project Structure

```text
.
├── youtube_vid_downloader.py  # Main interactive downloader script
├── requirements.txt           # Python dependencies (yt-dlp, imageio-ffmpeg)
├── .gitignore                 # Git ignore configuration
└── README.md                  # Project documentation
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
