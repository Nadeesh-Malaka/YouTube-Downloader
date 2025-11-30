import yt_dlp
import os
from typing import Dict, List, Optional

class YouTubeDownloader:
    def __init__(self, download_path: str = "./downloads"):
        self.download_path = download_path
        os.makedirs(download_path, exist_ok=True)
        
    def get_available_formats(self, url: str) -> Dict:
        """Get all available formats for a video"""
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return {
                'title': info_dict.get('title'),
                'duration': info_dict.get('duration'),
                'formats': info_dict.get('formats', [])
            }
    
    def download_video(self, url: str, quality: str = 'best', format_id: Optional[str] = None) -> str:
        """Download video only"""
        # Use format selection that avoids merging when ffmpeg is not available
        if format_id:
            format_string = format_id
        elif quality == 'best':
            format_string = 'best[ext=mp4]/best'
        else:
            # Only select pre-merged formats to avoid needing ffmpeg
            format_string = f'best[height<={quality}][ext=mp4]/best[height<={quality}]/best[ext=mp4]/best'
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'format': format_string,
            'noplaylist': True,  # Ensure single video download
            'ignoreerrors': False,  # Don't abort on errors, just report them
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return f"Video downloaded to {self.download_path}"
    
    def download_audio(self, url: str, quality: str = 'best') -> str:
        """Download audio only"""
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'quiet': False,
        }
        
        # Only add audio conversion if ffmpeg is available
        try:
            import shutil
            if shutil.which('ffmpeg'):
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }]
        except Exception:
            pass
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return f"Audio downloaded to {self.download_path}"
    
    def download_playlist(self, playlist_url: str, download_type: str = 'video', quality: str = 'best') -> str:
        """Download entire playlist"""
        if download_type == 'audio':
            return self.download_audio(playlist_url, quality)
        
        # Use format selection that avoids merging when ffmpeg is not available
        if quality == 'best':
            format_string = 'best[ext=mp4]/best'
        else:
            format_string = f'best[height<={quality}][ext=mp4]/best[height<={quality}]/best[ext=mp4]/best'
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'),
            'format': format_string,
            'ignoreerrors': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
            return f"Playlist downloaded to {self.download_path}"
    
    def select_quality_interactive(self, url: str) -> str:
        """Interactive quality selection"""
        formats = self.get_available_formats(url)
        print(f"\nAvailable formats for: {formats['title']}")
        print("ID\tResolution\tExtension\tFPS\tSize")
        print("-" * 50)
        
        video_formats = []
        for fmt in formats['formats']:
            if fmt.get('vcodec') != 'none' and fmt.get('height'):
                size = fmt.get('filesize_approx', 0)
                size_str = f"{size/1024/1024:.1f}MB" if size else "Unknown"
                print(f"{fmt['format_id']}\t{fmt['height']}p\t{fmt['ext']}\t{fmt.get('fps', 'N/A')}\t{size_str}")
                video_formats.append(fmt['format_id'])
        
        while True:
            choice = input("\nEnter format ID (or 'best' for highest quality): ").strip()
            if choice.lower() == 'best' or choice in video_formats:
                return choice
            print("Invalid format ID. Try again.")

def main():
    downloader = YouTubeDownloader()
    
    print("=== YouTube Downloader ===")
    print("1. Download video")
    print("2. Download audio")
    print("3. Download playlist")
    print("4. Show available formats")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '5':
            break
        elif choice == '4':
            url = input("Enter video URL: ").strip()
            downloader.get_available_formats(url)
        elif choice in ['1', '2', '3']:
            url = input("Enter URL: ").strip()
            
            if choice == '1':
                quality_choice = input("Auto quality (a) or select manually (m)? ").strip().lower()
                if quality_choice == 'm':
                    format_id = downloader.select_quality_interactive(url)
                    result = downloader.download_video(url, format_id=format_id)
                else:
                    quality = input("Enter max resolution (720, 1080, 1440, etc.) or 'best': ").strip()
                    result = downloader.download_video(url, quality)
                    
            elif choice == '2':
                quality = input("Audio quality (0-9, default 5): ").strip() or '5'
                result = downloader.download_audio(url, quality)
                
            elif choice == '3':
                download_type = input("Download type (video/audio): ").strip().lower()
                quality = input("Enter max resolution for video (720, 1080, etc.) or 'best': ").strip()
                result = downloader.download_playlist(url, download_type, quality)
            
            print(f"\n{result}")
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()