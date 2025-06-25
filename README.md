# Multi-Format Video and Audio Downloader

A powerful tool to download videos and audio from various platforms in different formats. This tool uses [yt-dlp](https://github.com/yt-dlp/yt-dlp), a feature-rich fork of youtube-dl.

Available in three versions:
1. **Command-line interface** - For terminal users
2. **Desktop GUI** - For desktop users
3. **Web interface** - For browser access and remote usage

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

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
- **Cookie bypass for restricted sites**:
  - Use cookies from browser (Chrome, Firefox, Safari, Edge, Opera)
  - Paste cookies in Netscape format
  - Extract cookies from browsers using the included utility
- **Advanced HTTP options**:
  - Custom User-Agent
  - Custom Referer
  - Custom HTTP headers

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
- `--cookies FILE`: Path to cookies file (Netscape or browser cookies.txt format)
- `--browser-cookies BROWSER`: Extract cookies from browser (chrome, firefox, safari, edge, opera)
- `--user-agent AGENT`: Specify a custom user agent
- `--referer URL`: Specify a custom referer, useful for bypassing some restrictions
- `--headers JSON`: Specify custom HTTP headers as a JSON string

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

### Bypassing Website Restrictions

Some websites require cookies or specific headers to download videos. Here's how to bypass these restrictions:

1. Using cookies from a browser:
   ```
   python multi_downloader.py --browser-cookies chrome https://www.example.com/restricted-video
   ```

2. Using a cookies file:
   ```
   python multi_downloader.py --cookies cookies.txt https://www.example.com/restricted-video
   ```

3. Using custom user agent and referer:
   ```
   python multi_downloader.py --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" --referer "https://www.example.com" https://www.example.com/restricted-video
   ```

4. Using custom HTTP headers:
   ```
   python multi_downloader.py --headers '{"X-Requested-With": "XMLHttpRequest", "Origin": "https://www.example.com"}' https://www.example.com/restricted-video
   ```

### Extracting Cookies

You can use the included `extract_cookies.py` script to extract cookies from browsers:

```
python extract_cookies.py chrome -d example.com -o cookies.txt
```

This will extract cookies from Chrome for the domain example.com and save them to cookies.txt.

## Supported Sites

This script supports all sites that yt-dlp supports, including:

- YouTube
- Vimeo
- Dailymotion
- Facebook
- Twitter
- Instagram
- SoundCloud

## Deployment

### Local Deployment

To run the web interface locally:

```
./run_local.sh
```

This will start the web server on port 8080. You can access it at http://localhost:8080.

### Render.com Deployment

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/djb3232/Ytytyt)

To deploy to Render.com:

1. Click the "Deploy to Render" button above, or
2. Follow these steps manually:
   - Fork this repository to your GitHub account
   - Sign up for a Render.com account
   - Connect your GitHub account to Render.com
   - Create a new Web Service in Render.com
   - Select your forked repository
   - Use the following settings:
     - Name: multi-format-downloader
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn web_downloader:app`
     - Add the following environment variables:
       - `PORT`: 10000
       - `SECRET_KEY`: (generate a random string)
       - `RENDER`: true

For detailed instructions, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).

## Supported Sites (continued)

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

## Web Interface

This project also includes a web interface that allows you to download videos and audio through your browser:

```
./run_web_server.sh
```

Or for production environments:

```
./run_production.sh
```

The web interface provides the following features:

- Access the downloader from any device with a web browser
- Download videos and audio with customizable options
- Track download progress in real-time
- Manage multiple downloads simultaneously
- Download completed files directly from the browser
- Responsive design that works on desktop and mobile devices

### Web Interface Screenshots

![Web Interface Screenshot](https://i.imgur.com/example2.png)

### Running on a Server

You can run the web interface on a server to access it remotely:

1. Clone the repository on your server
2. Install dependencies: `pip install -r requirements.txt`
3. Run the production server: `./run_production.sh`
4. Access the interface at `http://your-server-ip:12000`

You can change the port by setting the `PORT` environment variable:

```
PORT=8080 ./run_production.sh
```

## License

This project is open source and available under the MIT License.