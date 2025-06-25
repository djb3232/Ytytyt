# Multi-Format Video and Audio Downloader

A powerful script to download videos and audio from various platforms in different formats. This tool uses [yt-dlp](https://github.com/yt-dlp/yt-dlp), a feature-rich fork of youtube-dl.

Available in both command-line and graphical user interface versions.

## Features

- Download videos in various formats (mp4, webm, etc.)
- Download audio-only in various formats (mp3, m4a, opus, etc.)
- Specify quality (best, worst, 1080p, 720p, etc.)
- Download entire playlists
- Download with subtitles
- List available formats for a video
- Display video information
- Control download rate
- Proxy support

## Requirements

- Python 3.6 or higher
- yt-dlp (automatically installed if missing)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/djb3232/Ytytyt.git
   cd Ytytyt
   ```

2. Run the installation script:
   ```
   ./install.sh
   ```

   Or manually make the scripts executable:
   ```
   chmod +x multi_downloader.py download.sh gui_downloader.py
   ```

## Usage

```
python multi_downloader.py [options] URL [URL...]
```

### Options

- `-h, --help`: Show help message and exit
- `-f, --format FORMAT`: Specify output format (mp4, webm, mp3, m4a, etc.)
- `-q, --quality QUALITY`: Specify quality (best, worst, 1080, 720, etc.)
- `-o, --output TEMPLATE`: Output filename template
- `-a, --audio-only`: Download audio only
- `-p, --playlist`: Download all videos in a playlist
- `-s, --subtitles LANGS`: Download subtitles (comma separated language codes)
- `-l, --list-formats`: List available formats instead of downloading
- `-i, --info`: Display video info instead of downloading
- `--proxy URL`: Use the specified HTTP/HTTPS/SOCKS proxy
- `--limit-rate RATE`: Maximum download rate (e.g. 50K, 4.2M)
- `--no-mtime`: Don't use the Last-modified header to set the file modification time

## Examples

1. Download a video in best quality MP4 format:
   ```
   python multi_downloader.py -f mp4 -q best https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. Download audio only in MP3 format:
   ```
   python multi_downloader.py -a -f mp3 https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

3. Download a video in 720p quality:
   ```
   python multi_downloader.py -q 720 https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

4. Download a playlist:
   ```
   python multi_downloader.py -p https://www.youtube.com/playlist?list=PLexample
   ```

5. List available formats for a video:
   ```
   python multi_downloader.py -l https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

6. Download with English and Spanish subtitles:
   ```
   python multi_downloader.py -s en,es https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

7. Limit download rate:
   ```
   python multi_downloader.py --limit-rate 500K https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

## Advanced Usage

You can combine multiple options for more specific downloads:

```
python multi_downloader.py -f mp4 -q 1080 -s en -o "%(title)s-%(resolution)s.%(ext)s" https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

This will download a 1080p MP4 video with English subtitles and name the file using the video title and resolution.

## Supported Sites

This script supports all sites that yt-dlp supports, including:

- YouTube
- Vimeo
- Dailymotion
- Facebook
- Twitter
- Instagram
- SoundCloud
- And many more!

For a complete list, check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#supported-sites).

## Graphical User Interface

This project also includes a GUI version for those who prefer a graphical interface:

```
python gui_downloader.py
```

The GUI provides all the same functionality as the command-line version but in a more user-friendly interface:

- Input multiple URLs
- Select format and quality from dropdown menus
- Choose output directory with a file browser
- Set advanced options like proxy and rate limits
- View download progress in real-time
- List available formats and video information

![GUI Screenshot](https://i.imgur.com/example.png)

## License

This project is open source and available under the MIT License.