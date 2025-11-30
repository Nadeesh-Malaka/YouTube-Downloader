# YouTube Downloader

A simple and powerful YouTube video/audio downloader with both CLI and GUI interfaces, built with Python and yt-dlp.

## Features

- 📹 Download single videos in various qualities
- 🎵 Download audio only (MP3 format when ffmpeg is available)
- 📂 Download entire playlists
- 🎯 Interactive quality selection
- 🔍 View available formats before downloading
- ⚡ Works without ffmpeg (uses pre-merged formats)
- 🖥️ **Desktop GUI Application** - Easy to use graphical interface
- 💻 **CLI Version** - Command-line interface for advanced users
- 📦 **Standalone Executable** - Run without Python installed

## Two Versions Available

### 1. GUI Application (Recommended for most users)
- User-friendly graphical interface
- Real-time download progress
- Can be built as standalone .exe
- Run: `python gui_app.py`

### 2. CLI Application (For advanced users)
- Command-line interface
- Interactive menu system
- Run: `python main.py`

## Requirements

- Python 3.7+
- yt-dlp

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <repository-name>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Linux/Mac
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Quick Start

### Run GUI Application (Easiest)
```bash
python gui_app.py
```

### Run CLI Application
```bash
python main.py
```

## Building Standalone Executable

To create an .exe file that runs without Python:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --windowed --name="YouTubeDownloader" gui_app.py
```

3. Find your executable in the `dist` folder

**For detailed build instructions, see [BUILD_GUIDE.md](BUILD_GUIDE.md)**

### Menu Options

1. **Download Video** - Download a single video
   - Choose automatic quality selection or manual format selection
   - Specify max resolution (720, 1080, 1440, etc.) or 'best'

2. **Download Audio** - Extract audio only
   - Audio quality: 0-9 (default: 5)
   - Converts to MP3 if ffmpeg is installed

3. **Download Playlist** - Download entire YouTube playlist
   - Choose video or audio format
   - All videos saved in a playlist folder

4. **Show Available Formats** - View all available formats for a video

5. **Exit** - Close the application

## Examples

### Download a video in 720p
```
Choice: 1
URL: https://youtu.be/VIDEO_ID
Quality: a
Resolution: 720
```

### Download audio only
```
Choice: 2
URL: https://youtu.be/VIDEO_ID
Quality: 5
```

### Download playlist
```
Choice: 3
URL: https://www.youtube.com/playlist?list=PLAYLIST_ID
Type: video
Resolution: 1080
```

## Optional: Install ffmpeg

For better quality and audio conversion features:

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to PATH
3. Or use: `winget install ffmpeg`

**Linux:**
```bash
sudo apt install ffmpeg  # Debian/Ubuntu
sudo yum install ffmpeg  # CentOS/RHEL
```

**Mac:**
```bash
brew install ffmpeg
```

## Downloads Location

All downloads are saved to the `./downloads` folder by default.

## Notes

- The script works without ffmpeg by using pre-merged video formats
- Some formats may require ffmpeg for merging video and audio streams
- Playlist downloads are organized in separate folders

## Troubleshooting

### "No JavaScript runtime found" warning
This is a warning from yt-dlp. The script will still work. To fix:
- Install Node.js from https://nodejs.org/

### Lower video quality than expected
- Install ffmpeg for access to higher quality separate video/audio streams
- YouTube may not have higher quality versions for some videos

## License

MIT License - Feel free to use and modify

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws.
