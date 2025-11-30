# YouTube Downloader

A simple and powerful YouTube video/audio downloader built with Python and yt-dlp.

## Features

- 📹 Download single videos in various qualities
- 🎵 Download audio only (MP3 format when ffmpeg is available)
- 📂 Download entire playlists
- 🎯 Interactive quality selection
- 🔍 View available formats before downloading
- ⚡ Works without ffmpeg (uses pre-merged formats)

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
pip install yt-dlp
```

## Usage

Run the script:
```bash
python main.py
```

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
