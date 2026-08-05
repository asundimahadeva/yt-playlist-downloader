---
name: repo-architecture
description: "How repo is organized and where a change belongs: modules, entry points, data flow, and common task recipes. Modules: cli-downloader (youtube_vid_downloader.py)."
---

<!-- generated-by: skillgen v0.0.0-dev | repo: repo | commit: f737675036d9d1db94d35b4fe4716112d9e30dbd | date: 2026-08-05T18:25:47Z -->
# Architecture

## Overview
A single-file interactive Python CLI that uses yt-dlp and ffmpeg to download YouTube videos and playlists, letting users choose quality, subtitles, chapter handling, and save location, and generating an HTML chapter dashboard.

**Architecture style:** single-script layered CLI (monolithic, no packages)

## Directory map
| Path | Purpose |
|---|---|
| `README.md` | Documentation for installation, usage, features, and troubleshooting. |
| `requirements.txt` | Pinned dependencies for yt-dlp-based downloading and related tooling. |
| `youtube_vid_downloader.py` | Primary CLI application implementing video/playlist download workflow, user interaction, and chapter HTML generation. |

## Entry points
- `youtube_vid_downloader.py` — Interactive CLI entry point: prompts for URL, quality, subtitles, chapters, and orchestrates downloads and post-processing.

## Data & control flow
User starts the CLI, which prompts for a YouTube URL and options (quality, subtitles, chapter mode, target directory). The script resolves ffmpeg path, configures yt-dlp download parameters, downloads videos or playlist entries, embeds subtitles and chapters as requested, collects metadata, and finally generates a CHAPTERS.html dashboard in the output directory.

## Cross-cutting concerns
Configuration is mostly interactive via prompts with some defaults; error handling uses try/except blocks and simple messages. Logging is via print-based progress output. No auth, persistence layer, or global configuration files are present.

## External integrations
- yt-dlp (YouTube download and metadata extraction)
- ffmpeg (media processing, merging, and embedding subtitles/chapters)
- Local filesystem (selecting save directories, writing downloaded media and CHAPTERS.html)

## Module inventory
| Module | Paths | Responsibility | Key dependencies |
|---|---|---|---|
| cli-downloader | `youtube_vid_downloader.py` | Implements the interactive YouTube download workflow, including user prompts, download orchestration, and HTML chapter dashboard generation. | yt_dlp, ffmpeg (invoked via filesystem/path resolution), os, sys, pathlib or similar stdlib modules (for directories and paths) |

## Module dependency notes
There is effectively a single internal module: the main CLI script. Helper functions like clean_filename, get_ffmpeg_path, format_time, parse_description_chapters, select_save_directory, select_quality, select_subtitles, select_chapter_mode, generate_chapters_html are defined and used within the same file. No intra-repo imports or multi-layer package structure exist; external dependencies yt-dlp and ffmpeg are used directly from this script.

## Common tasks

### Add an audio-only download mode (MP3/M4A) to the interactive CLI

1. Extend the interactive prompts to let the user choose between video (current behavior) and audio-only mode, following the pattern used in select_quality(). Add a new helper like select_download_mode() near other prompt helpers. — `youtube_vid_downloader.py`
2. Implement select_download_mode() in youtube_vid_downloader.py that prints options (e.g., 1. Video MP4 [Default], 2. Audio-only M4A, 3. Audio-only MP3) and returns a mode identifier string similar to select_chapter_mode(). Use the existing prompt style (print banner, input with default). — `youtube_vid_downloader.py`
3. In main(), after format_spec = select_quality(), call the new select_download_mode() and store its result (e.g., download_mode). Use this to adjust ydl_opts before constructing the YoutubeDL instance. — `youtube_vid_downloader.py`
4. Modify ydl_opts in main() so that when download_mode indicates audio-only, set an appropriate yt-dlp format string (e.g., 'bestaudio/bestaudio[ext=m4a]') instead of the video-oriented format_spec currently returned by select_quality(). You can follow how subtitles and chapter_mode branches already update ydl_opts. — `youtube_vid_downloader.py`
5. For MP3 output, add an FFmpegExtractAudio postprocessor to ydl_opts['postprocessors'], using the existing postprocessors list as precedent. For example, when download_mode == 'mp3', append {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'} to postprocessors before assigning ydl_opts['postprocessors']. — `youtube_vid_downloader.py`
6. Adjust merge_output_format and output_template conditionally: for audio-only downloads, set merge_output_format to None or remove it and ensure outtmpl ends with .%(ext)s to allow audio extensions (similar to existing playlist vs single video output_template logic). — `youtube_vid_downloader.py`
7. Update automatic cleanup logic to avoid deleting the resulting audio files: keep temp_extensions as-is but verify that extensions like '.m4a' are not treated as temporary when they are the primary output format in audio-only mode. You may need to conditionally skip '.m4a' from temp_extensions when download_mode is audio-only. — `youtube_vid_downloader.py`
8. Document the new audio-only mode in README.md under Features and Usage, mirroring the style of the existing bullet points for Quality Selection and Subtitles and adding an example workflow that mentions the new prompt. — `README.md`

Verify: Run `python youtube_vid_downloader.py`, choose a YouTube URL, select audio-only mode, and confirm that the output in the target folder is an audio file (M4A/MP3) and that subtitles/chapter embedding behave sensibly for audio-only.

### Add a non-interactive CLI mode with command-line arguments for URL and options

1. Import argparse or use sys.argv parsing at the top of youtube_vid_downloader.py, placing the new import near existing imports (os, sys, re, yt_dlp, imageio_ffmpeg). — `youtube_vid_downloader.py`
2. Design a small argument parser function (e.g., parse_args()) in youtube_vid_downloader.py that supports flags like --url, --quality, --embed-subs, --chapter-mode, and --output-dir. Use select_quality() and select_chapter_mode() as references for allowable values. — `youtube_vid_downloader.py`
3. Refactor main() minimally so it can operate either in interactive mode (current behavior) or non-interactive mode when arguments are provided. For example, detect if --url is present: when args.url is set, skip input() calls and use the argument values instead, mapping them through select_quality() or direct dictionaries as needed. — `youtube_vid_downloader.py`
4. Wire argument values into existing variables: set url, base_dir, format_spec, embed_subs, and chapter_mode from parsed args, falling back to interactive prompts when these args are missing. Keep current interactive banners and messages as the default path. — `youtube_vid_downloader.py`
5. Ensure that get_ffmpeg_path(), the metadata fetch block using yt_dlp.YoutubeDL, and subsequent ydl_opts construction remain unchanged in structure; only their inputs (url, base_dir, etc.) should be overridable via arguments. — `youtube_vid_downloader.py`
6. Update the __main__ guard at the bottom of youtube_vid_downloader.py so that it calls parse_args() and passes arguments to main(), or so that main() internally calls parse_args(); follow the existing pattern where main() is the single entry point. — `youtube_vid_downloader.py`
7. Add a Usage section to README.md documenting the new non-interactive mode, including example commands like `python youtube_vid_downloader.py --url <VIDEO_URL> --quality 1080p --embed-subs yes --chapter-mode embed --output-dir ~/Downloads/MyVideos`. — `README.md`

Verify: Run `python youtube_vid_downloader.py --url <some YouTube URL> --quality 720p --embed-subs n --chapter-mode 3 --output-dir ./test_out` and confirm that the script runs without interactive prompts, downloads to ./test_out, and honors the provided options.

### Extend CHAPTERS.html to include thumbnail previews and total video duration

1. Study generate_chapters_html() in youtube_vid_downloader.py to see how video_info_list entries are used (title, webpage_url, chapters, description) and how cards_html is assembled using HTML/CSS strings. — `youtube_vid_downloader.py`
2. Update generate_chapters_html() to extract thumbnail URLs and duration from each video entry. yt-dlp info dicts typically have 'thumbnail' and 'duration' keys; access them similarly to how 'title' and 'webpage_url' are accessed. — `youtube_vid_downloader.py`
3. Use format_time() as a precedent to convert duration seconds to a human-readable string. If duration is missing, fall back to 'Unknown' or a similar label. — `youtube_vid_downloader.py`
4. Modify the HTML template inside generate_chapters_html() so each card includes a thumbnail image element (e.g., <img src="..." class="thumb" />) and a duration line. Adjust the CSS within the <style> block to style .thumb appropriately (size, border-radius) and to add a small muted duration text using the existing .text-muted style or similar. — `youtube_vid_downloader.py`
5. Ensure that when thumbnail or duration data is not present, the HTML still renders gracefully (e.g., conditional inclusion, placeholder image, or skipping the img tag). Follow the existing pattern used for chapters where a 'No timestamped chapters found' message is shown. — `youtube_vid_downloader.py`
6. Confirm that generate_chapters_html() is still called from main() after downloads finish and that video_entries contains the necessary data (title, webpage_url, thumbnail, duration). If metadata fetch does not include thumbnails or duration for some entries, consider adding 'skip_download': True but ensure metadata richness is preserved as it is now. — `youtube_vid_downloader.py`
7. Update README.md Features section describing the CHAPTERS.html dashboard to mention thumbnail previews and video durations, mirroring the style of the current bullet for 'Interactive CHAPTERS.html Index'. — `README.md`

Verify: Run `python youtube_vid_downloader.py` on a playlist, open the generated CHAPTERS.html in a browser, and confirm that each video card shows a thumbnail image and a readable total duration alongside the existing title and chapters list.

### Support subtitle language selection instead of hard-coded English

1. Inspect select_subtitles() in youtube_vid_downloader.py to see the current behavior (only a yes/no prompt for embedding English subtitles). Note how embed_subs controls ydl_opts['writesubtitles'] and 'subtitleslangs' later in main(). — `youtube_vid_downloader.py`
2. Extend select_subtitles() to ask the user which subtitle language(s) they want when they choose to embed subtitles. For example, prompt for a language code (e.g., 'en', 'es', 'de') or 'auto' for automatic matches, returning both a boolean flag and a list of language patterns. — `youtube_vid_downloader.py`
3. Modify main() assignment so embed_subs can carry language information: either change embed_subs to a tuple (embed_flag, languages) or introduce a separate variable like subtitles_langs returned from an enhanced select_subtitles(). — `youtube_vid_downloader.py`
4. Update the subtitles configuration block in main() where ydl_opts is updated. Instead of hardcoding 'subtitleslangs': ['en.*', 'en'], use the language list returned from select_subtitles() (e.g., ['es.*', 'es']). Keep 'writesubtitles' and 'writeautomaticsub' logic similar to the existing pattern. — `youtube_vid_downloader.py`
5. Ensure FFmpegEmbedSubtitle postprocessor remains appended to postprocessors when subtitles are requested, reusing the existing precedent in youtube_vid_downloader.py. — `youtube_vid_downloader.py`
6. Handle invalid or empty language input gracefully by defaulting to English (current behavior) or by skipping subtitle embedding. Follow the fallback pattern used in select_chapter_mode() where invalid choices revert to '1'. — `youtube_vid_downloader.py`
7. Document the new subtitle language selection in README.md, updating the 'Embedded Closed Captions (Subtitles)' feature description and adding a short example interaction showing language input (e.g., 'Enter subtitle language code [Default: en]'). — `README.md`

Verify: Run `python youtube_vid_downloader.py`, choose to embed subtitles, enter a non-English language code (e.g., 'es'), download a video that has Spanish subtitles, and confirm that the resulting MP4 contains the selected subtitles rather than only English.

### Add a configuration section for default download directory and quality

1. Review select_save_directory() and select_quality() in youtube_vid_downloader.py to see how defaults (Downloads folder and 1080p) are currently hardcoded and how user input overrides them. — `youtube_vid_downloader.py`
2. Introduce a small configuration block at the top of youtube_vid_downloader.py (e.g., DEFAULT_DOWNLOAD_DIR, DEFAULT_QUALITY_CHOICE) or load from a simple config file (like config.json) located in the same directory. Start with constants to keep the script monolithic as it is now. — `youtube_vid_downloader.py`
3. Update select_save_directory() so its displayed default folder uses the new configuration value instead of always os.path.join(os.path.expanduser("~"), "Downloads"). Keep the path expansion and os.makedirs logic the same. — `youtube_vid_downloader.py`
4. Update select_quality() so its default choice (currently hardcoded to '1') can be derived from a config value (e.g., DEFAULT_QUALITY_CHOICE). Ensure the quality_map dictionary is still used and that unexpected config values fall back to '1'. — `youtube_vid_downloader.py`
5. If using an external config file (e.g., config.json), add logic near the top of youtube_vid_downloader.py to read it safely, handle missing file or fields gracefully, and populate configuration variables with sensible defaults. Use existing safe patterns such as try/except used in get_ffmpeg_path(). — `youtube_vid_downloader.py`
6. Optionally expose a simple CLI flag (e.g., --reset-config or --print-config) using the same argument parsing strategy as the non-interactive mode recipe, allowing users to see or override defaults. — `youtube_vid_downloader.py`
7. Describe configuration behavior in README.md: add a 'Configuration' section explaining how default download directory and quality are determined, how to edit the config file or constants, and how they interact with interactive prompts. — `README.md`

Verify: Set custom defaults in the configuration (e.g., a different folder and 720p), run `python youtube_vid_downloader.py` without changing the prompts’ default responses, and confirm that downloads go to the configured folder and use the configured quality.

### Add an option to skip CHAPTERS.html generation

1. Review how generate_chapters_html() is called in main() in youtube_vid_downloader.py: currently, after cleanup, there is a conditional `if video_entries:` that always generates CHAPTERS.html. — `youtube_vid_downloader.py`
2. Add a new interactive prompt helper (e.g., select_chapters_html_mode() or include_chapters_html()) near select_chapter_mode() that asks the user whether they want the CHAPTERS.html dashboard generated (y/n) with a default of 'y'. — `youtube_vid_downloader.py`
3. Call this new helper inside main(), store the result in a variable like generate_html, and use it to guard the call to generate_chapters_html(): change the `if video_entries:` condition to `if video_entries and generate_html:`. — `youtube_vid_downloader.py`
4. Ensure that skipping HTML generation does not affect the rest of the logic: cleanup of temp files, final completion messages, and playlist folder creation should remain intact. — `youtube_vid_downloader.py`
5. If non-interactive mode is implemented (see separate recipe), add a corresponding CLI flag (e.g., --no-html) that sets generate_html to False when provided. Use the same patterns as --chapter-mode or other flags. — `youtube_vid_downloader.py`
6. Update README.md to mention that CHAPTERS.html generation can be disabled via the new prompt or flag, and document a use case (e.g., when the user only needs local files and not an HTML dashboard). — `README.md`

Verify: Run `python youtube_vid_downloader.py`, select 'no' when asked about generating CHAPTERS.html, and confirm that no CHAPTERS.html file appears in the output folder while downloads and chapter embedding still work as before.

### Improve error handling and progress reporting (e.g., retries, clearer messages)

1. Inspect existing error handling in youtube_vid_downloader.py, notably get_ffmpeg_path() (try/except), the metadata fetch block around ydl.extract_info(), and the cleanup section where os.remove is wrapped in a broad try/except. — `youtube_vid_downloader.py`
2. Add clearer user-facing messages around the metadata fetch try/except in main(), such as indicating whether the URL could not be resolved or suggesting checking the network connection. Use print() consistently with the current style of informational messages. — `youtube_vid_downloader.py`
3. Implement a simple retry mechanism for the metadata fetch: after a failure, optionally prompt the user to retry or exit, and call ydl.extract_info() again if they choose to retry. Keep the logic within the existing with yt_dlp.YoutubeDL(ydl_opts_meta) context. — `youtube_vid_downloader.py`
4. Wrap the main download call `ydl.download([url])` in a try/except block to catch yt_dlp-specific errors and print a clear error message, possibly including the URL and a hint to check the requirements or ffmpeg installation. — `youtube_vid_downloader.py`
5. Enable more visible progress reporting by configuring yt_dlp’s 'progress_hooks' or less quiet behavior. For example, remove 'quiet': True from ydl_opts_meta or add a custom hook function defined in youtube_vid_downloader.py that prints simple status updates (e.g., "Downloading: <title>"), following yt-dlp’s documented pattern. — `youtube_vid_downloader.py`
6. Ensure that the final success banner in main() ("Download & Processing Complete!") is only printed when the main download block succeeded; on failure, print a different message and avoid implying success. — `youtube_vid_downloader.py`
7. Document improved error handling and progress behavior in README.md, possibly adding a short 'Troubleshooting' section that describes common failure modes (e.g., missing ffmpeg, invalid URL) and how the script reports them. — `README.md`

Verify: Intentionally provide an invalid URL and run `python youtube_vid_downloader.py`; observe that the script prints clear error messages and offers retry or exit. Then run with a valid URL and confirm that progress messages appear and the completion banner is shown only after successful download.

### Add a basic dry-run mode verifying yt-dlp and ffmpeg availability

1. Review get_ffmpeg_path() in youtube_vid_downloader.py to see how ffmpeg is currently located (via imageio_ffmpeg.get_ffmpeg_exe()) and how failures fall back to 'ffmpeg'. Also note that yt-dlp is imported at the top and used directly without explicit availability checks. — `youtube_vid_downloader.py`
2. Add a new helper function (e.g., run_dry_run_check()) in youtube_vid_downloader.py that calls get_ffmpeg_path(), attempts to run a simple ffmpeg command like `ffmpeg -version` via os.system or subprocess, and tries a quick yt-dlp operation like printing its version (`yt_dlp.__version__`). Handle exceptions and non-zero exit codes gracefully, printing diagnostic messages. — `youtube_vid_downloader.py`
3. Expose a CLI flag for dry-run in the argument parser (if implemented) or add an early interactive option that lets the user run a system check before actual downloads. For example, if `--dry-run` is present, call run_dry_run_check() and exit without asking for a URL. — `youtube_vid_downloader.py`
4. Ensure that dry-run mode does not create output directories, download any files, or generate CHAPTERS.html. It should only probe environment capabilities and report success/failure. — `youtube_vid_downloader.py`
5. Use existing messaging patterns (print banners and separators similar to the main banner in main()) to make dry-run output easy to read and consistent with the rest of the CLI. — `youtube_vid_downloader.py`
6. Update README.md with a new section or note describing the dry-run capability, including example usage (`python youtube_vid_downloader.py --dry-run`) and explaining what checks are performed. — `README.md`

Verify: Run `python youtube_vid_downloader.py --dry-run` (or the equivalent interactive option), confirm that it reports yt-dlp and ffmpeg availability and exits without downloading anything or creating new files.

*See also: `repo-tech-stack` for commands/conventions, `repo-modules` for per-module guides.*

*Verified claims: 5/6; 1 unverifiable claim(s) removed.*

---
*Generated by skillgen. Regenerate with `skillgen scan <repo>`.*
