import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import yt_dlp
import os
from typing import Optional
import sys
import re

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x550")
        self.root.resizable(True, True)
        self.root.minsize(550, 500)
        
        # Modern color scheme - Darker theme
        self.colors = {
            'bg': '#0f0f0f',
            'fg': '#ffffff',
            'accent': '#ff0000',
            'secondary': '#1a1a1a',
            'button': '#ff0000',
            'button_hover': '#cc0000',
            'success': '#00c853',
            'text_bg': '#262626',
            'border': '#333333'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Default download path
        self.download_path = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_path, exist_ok=True)
        
        # Download state
        self.is_downloading = False
        self.current_download = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure ttk widgets
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TRadiobutton', background=self.colors['bg'], foreground=self.colors['fg'])
        style.map('TRadiobutton', background=[('active', self.colors['secondary'])])
        
        # Create main canvas and scrollbar
        canvas = tk.Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        
        # Create scrollable frame
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Center the content in canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
        
        def _configure_canvas(event):
            # Center the scrollable frame and allow it to expand up to 800px
            max_width = 800
            # Calculate content width with proper margins
            if event.width < 640:
                # For smaller windows, use most of the width
                content_width = event.width - 40
            else:
                # For larger windows, expand up to max_width
                content_width = min(event.width - 100, max_width)
            
            canvas.itemconfig(canvas_window, width=content_width)
            canvas.coords(canvas_window, event.width / 2, 0)
        
        canvas.bind('<Configure>', _configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Main container with padding - will be centered
        main_container = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        main_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Compact Title - centered
        title_frame = tk.Frame(main_container, bg=self.colors['bg'])
        title_frame.pack(pady=(0, 8))
        
        title_label = tk.Label(
            title_frame, 
            text="▶ YouTube Downloader", 
            font=("Segoe UI", 16, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # URL Input - Very Compact
        url_frame = tk.LabelFrame(
            main_container, 
            text=" 🔗 URL ",
            font=("Segoe UI", 9, "bold"),
            fg="#cccccc",
            bg=self.colors['secondary'],
            borderwidth=1,
            relief="solid"
        )
        url_frame.pack(pady=5, fill="x")
        
        url_inner = tk.Frame(url_frame, bg=self.colors['secondary'])
        url_inner.pack(padx=8, pady=5, fill="x")
        
        self.url_entry = tk.Entry(
            url_inner,
            font=("Segoe UI", 9),
            bg=self.colors['text_bg'],
            fg=self.colors['fg'],
            insertbackground=self.colors['accent'],
            relief="flat",
            borderwidth=0
        )
        self.url_entry.pack(fill="x", ipady=4)
        
        # Download Type - Compact with icons only
        type_frame = tk.LabelFrame(
            main_container,
            text=" 📋 Type ",
            font=("Segoe UI", 9, "bold"),
            fg="#cccccc",
            bg=self.colors['secondary'],
            borderwidth=1,
            relief="solid"
        )
        type_frame.pack(pady=5, fill="x")
        
        type_inner = tk.Frame(type_frame, bg=self.colors['secondary'])
        type_inner.pack(padx=8, pady=5)
        
        self.download_type = tk.StringVar(value="video")
        self.download_type.trace('w', self.on_download_type_change)
        
        # Compact radio buttons
        for text, value in [("🎬 Video", "video"), ("🎵 Audio", "audio"), ("📂 Playlist", "playlist")]:
            rb = tk.Radiobutton(
                type_inner,
                text=text,
                variable=self.download_type,
                value=value,
                font=("Segoe UI", 9),
                bg=self.colors['secondary'],
                fg=self.colors['fg'],
                selectcolor=self.colors['text_bg'],
                activebackground=self.colors['secondary'],
                activeforeground=self.colors['accent'],
                borderwidth=0,
                highlightthickness=0
            )
            rb.pack(side="left", padx=8)
        
        # Quality - Compact inline
        self.quality_frame = tk.LabelFrame(
            main_container,
            text=" ⚙ Quality ",
            font=("Segoe UI", 9, "bold"),
            fg="#cccccc",
            bg=self.colors['secondary'],
            borderwidth=1,
            relief="solid"
        )
        self.quality_frame.pack(pady=5, fill="x")
        
        quality_inner = tk.Frame(self.quality_frame, bg=self.colors['secondary'])
        quality_inner.pack(padx=8, pady=5, fill="x")
        
        # Video quality section - horizontal
        self.video_quality_container = tk.Frame(quality_inner, bg=self.colors['secondary'])
        self.video_quality_container.pack(side="left", padx=(0, 15))
        
        tk.Label(
            self.video_quality_container,
            text="📺",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg=self.colors['secondary']
        ).pack(side="left", padx=(0, 5))
        
        self.quality_var = tk.StringVar(value="720")
        quality_options = ["360", "480", "720", "1080", "1440", "2160", "best"]
        
        # Style combobox for better visibility
        style.configure('Quality.TCombobox',
                       fieldbackground=self.colors['text_bg'],
                       background=self.colors['text_bg'],
                       foreground='#ffffff',
                       borderwidth=0,
                       arrowcolor='#ffffff')
        style.map('Quality.TCombobox',
                 fieldbackground=[('readonly', self.colors['text_bg'])],
                 selectbackground=[('readonly', self.colors['text_bg'])],
                 selectforeground=[('readonly', '#ffffff')])
        
        self.quality_combo = ttk.Combobox(
            self.video_quality_container,
            textvariable=self.quality_var,
            values=quality_options,
            state="readonly",
            width=8,
            font=("Segoe UI", 9),
            style='Quality.TCombobox'
        )
        self.quality_combo.pack(side="left")
        
        # Audio quality section
        self.audio_quality_container = tk.Frame(quality_inner, bg=self.colors['secondary'])
        
        tk.Label(
            self.audio_quality_container,
            text="🎵 Quality:",
            font=("Segoe UI", 9),
            fg="#ffffff",
            bg=self.colors['secondary']
        ).pack(side="left", padx=(0, 5))
        
        self.audio_quality_var = tk.StringVar(value="5")
        self.audio_quality_entry = tk.Entry(
            self.audio_quality_container,
            textvariable=self.audio_quality_var,
            width=5,
            font=("Segoe UI", 9),
            bg=self.colors['text_bg'],
            fg='#ffffff',
            insertbackground=self.colors['accent'],
            relief="flat",
            borderwidth=0
        )
        self.audio_quality_entry.pack(side="left", ipady=3)
        
        # Download Path - Very Compact
        path_frame = tk.LabelFrame(
            main_container,
            text=" 💾 Save ",
            font=("Segoe UI", 9, "bold"),
            fg="#cccccc",
            bg=self.colors['secondary'],
            borderwidth=1,
            relief="solid"
        )
        path_frame.pack(pady=5, fill="x")
        
        path_inner = tk.Frame(path_frame, bg=self.colors['secondary'])
        path_inner.pack(padx=8, pady=5, fill="x")
        
        self.path_entry = tk.Entry(
            path_inner,
            font=("Segoe UI", 8),
            bg=self.colors['text_bg'],
            fg=self.colors['fg'],
            insertbackground=self.colors['accent'],
            relief="flat",
            borderwidth=0
        )
        self.path_entry.insert(0, self.download_path)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=3)
        
        browse_btn = tk.Button(
            path_inner,
            text="📁",
            command=self.browse_folder,
            bg=self.colors['success'],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=8,
            pady=2
        )
        browse_btn.pack(side="left")
        browse_btn.bind("<Enter>", lambda e: browse_btn.config(bg="#00e676"))
        browse_btn.bind("<Leave>", lambda e: browse_btn.config(bg=self.colors['success']))
        
        # Very Compact Download Button
        self.download_btn = tk.Button(
            main_container,
            text="⬇ START",
            command=self.start_download,
            bg=self.colors['button'],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            pady=8
        )
        self.download_btn.pack(pady=8, fill="x")
        self.download_btn.bind("<Enter>", lambda e: self.download_btn.config(bg=self.colors['button_hover']) if not self.is_downloading else None)
        self.download_btn.bind("<Leave>", lambda e: self.download_btn.config(bg=self.colors['button']) if not self.is_downloading else None)
        
        # Compact Progress Section
        progress_frame = tk.LabelFrame(
            main_container,
            text=" 📊 Progress ",
            font=("Segoe UI", 9, "bold"),
            fg="#cccccc",
            bg=self.colors['secondary'],
            borderwidth=1,
            relief="solid"
        )
        progress_frame.pack(pady=5, fill="both", expand=True)
        
        progress_inner = tk.Frame(progress_frame, bg=self.colors['secondary'])
        progress_inner.pack(padx=8, pady=5, fill="both", expand=True)
        
        # Progress bar
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor=self.colors['text_bg'],
                       background=self.colors['accent'],
                       bordercolor=self.colors['secondary'],
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
        self.progress_bar = ttk.Progressbar(
            progress_inner,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar",
            length=300
        )
        self.progress_bar.pack(fill="x", pady=(0, 4))
        
        # Status label - more visible
        self.status_label = tk.Label(
            progress_inner,
            text="Ready",
            font=("Segoe UI", 8),
            fg="#aaaaaa",
            bg=self.colors['secondary']
        )
        self.status_label.pack(pady=(0, 4))
        
        # Very compact progress text
        self.progress_text = scrolledtext.ScrolledText(
            progress_inner,
            height=6,
            font=("Consolas", 8),
            bg=self.colors['text_bg'],
            fg='#00ff00',
            relief="flat",
            borderwidth=0,
            insertbackground=self.colors['accent']
        )
        self.progress_text.pack(fill="both", expand=True)
        
        # Initialize quality visibility
        self.on_download_type_change()
        
    def on_download_type_change(self, *args):
        """Update quality settings visibility based on download type"""
        download_type = self.download_type.get()
        
        if download_type == "audio":
            # Hide video quality, show audio quality
            self.video_quality_container.pack_forget()
            self.audio_quality_container.pack(side="left", padx=(0, 20))
        elif download_type == "video":
            # Show video quality, hide audio quality
            self.video_quality_container.pack(side="left", padx=(0, 20))
            self.audio_quality_container.pack_forget()
        else:  # playlist
            # Show both
            self.video_quality_container.pack(side="left", padx=(0, 20))
            self.audio_quality_container.pack_forget()
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            
    def log_message(self, message):
        """Add message to progress text widget - thread-safe"""
        def update():
            self.progress_text.insert(tk.END, message + "\n")
            self.progress_text.see(tk.END)
        self.root.after(0, update)
    
    def update_status(self, message, color="#aaaaaa"):
        """Update status label - thread-safe"""
        def update():
            self.status_label.config(text=message, fg=color)
        self.root.after(0, update)
    
    def update_progress_bar(self, value):
        """Update progress bar - thread-safe"""
        def update():
            self.progress_bar['value'] = value
        self.root.after(0, update)
        
    def progress_hook(self, d):
        """Hook for yt-dlp progress updates"""
        if d['status'] == 'downloading':
            # Extract progress information
            try:
                # Get raw data
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                # Calculate percentage
                if total > 0:
                    percent = (downloaded / total) * 100
                    self.update_progress_bar(percent)
                    
                    # Format data
                    downloaded_mb = downloaded / (1024 * 1024)
                    total_mb = total / (1024 * 1024)
                    
                    if speed:
                        speed_mb = speed / (1024 * 1024)
                        speed_str = f"{speed_mb:.2f} MB/s"
                    else:
                        speed_str = "N/A"
                    
                    if eta:
                        eta_min = eta // 60
                        eta_sec = eta % 60
                        eta_str = f"{int(eta_min)}m {int(eta_sec)}s"
                    else:
                        eta_str = "N/A"
                    
                    # Update status
                    status_msg = f"📥 {percent:.1f}% | {downloaded_mb:.1f}/{total_mb:.1f} MB | ⚡ {speed_str} | ⏱ {eta_str}"
                    self.update_status(status_msg, "#00ff00")
                    
                    # Log every 5%
                    if not hasattr(self, '_last_log_percent'):
                        self._last_log_percent = 0
                    
                    if percent - self._last_log_percent >= 5 or percent >= 99:
                        self.log_message(status_msg)
                        self._last_log_percent = percent
                else:
                    # Fallback for unknown size
                    downloaded_mb = downloaded / (1024 * 1024)
                    status_msg = f"📥 Downloaded: {downloaded_mb:.1f} MB"
                    self.update_status(status_msg, "#00ff00")
                    
            except Exception as e:
                # Fallback to basic display
                percent_str = d.get('_percent_str', '0%').strip()
                speed_str = d.get('_speed_str', 'N/A').strip()
                eta_str = d.get('_eta_str', 'N/A').strip()
                
                try:
                    percent = float(percent_str.replace('%', ''))
                    self.update_progress_bar(percent)
                except:
                    pass
                
                status_msg = f"📥 {percent_str} | Speed: {speed_str} | ETA: {eta_str}"
                self.update_status(status_msg, "#00ff00")
            
        elif d['status'] == 'finished':
            self.update_progress_bar(100)
            self.update_status("✓ Download finished, processing...", self.colors['success'])
            self.log_message("✅ Download complete, processing file...")
        
        elif d['status'] == 'error':
            self.update_status("✗ Download error", "#ff4444")
            self.log_message(f"❌ Error: {d.get('error', 'Unknown error')}")
            
    def download_video(self, url: str, quality: str) -> str:
        if quality == 'best':
            format_string = 'best[ext=mp4]/best'
        else:
            format_string = f'best[height<={quality}][ext=mp4]/best[height<={quality}]/best[ext=mp4]/best'
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'format': format_string,
            'noplaylist': True,
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return f"Video saved: {os.path.basename(filename)}"
    
    def download_audio(self, url: str, quality: str) -> str:
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': False,
        }
        
        # Check if ffmpeg is available
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
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if 'postprocessors' in ydl_opts:
                filename = os.path.splitext(filename)[0] + '.mp3'
            return f"Audio saved: {os.path.basename(filename)}"
    
    def download_playlist(self, url: str, quality: str, dl_type: str) -> str:
        if dl_type == 'audio':
            return self.download_audio(url, quality)
        
        if quality == 'best':
            format_string = 'best[ext=mp4]/best'
        else:
            format_string = f'best[height<={quality}][ext=mp4]/best[height<={quality}]/best[ext=mp4]/best'
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'),
            'format': format_string,
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            playlist_title = info.get('title', 'playlist')
            return f"Playlist saved: {playlist_title}"
    
    def download_thread(self):
        try:
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a YouTube URL")
                return
            
            self.progress_text.delete(1.0, tk.END)
            self.progress_bar['value'] = 0
            self._last_log_percent = 0
            
            self.log_message("="*60)
            self.log_message("🚀 Starting download...")
            self.log_message(f"📎 URL: {url}")
            self.log_message("="*60 + "\n")
            
            self.update_status("Preparing download...", self.colors['accent'])
            
            download_type = self.download_type.get()
            quality = self.quality_var.get()
            audio_quality = self.audio_quality_var.get()
            
            if download_type == "video":
                self.log_message(f"📹 Download Type: Video ({quality}p)")
                result = self.download_video(url, quality)
            elif download_type == "audio":
                self.log_message(f"🎵 Download Type: Audio (Quality: {audio_quality})")
                result = self.download_audio(url, audio_quality)
            elif download_type == "playlist":
                self.log_message(f"📂 Download Type: Playlist ({quality}p)")
                result = self.download_playlist(url, quality, "video")
            
            self.progress_bar['value'] = 100
            self.log_message("\n" + "="*60)
            self.log_message("✅ SUCCESS!")
            self.log_message(f"📁 {result}")
            self.log_message("="*60)
            
            self.update_status("✓ Download completed successfully!", self.colors['success'])
            messagebox.showinfo("Success", "Download completed successfully!")
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_message("\n" + "="*60)
            self.log_message(f"❌ ERROR: {str(e)}")
            self.log_message("="*60)
            self.update_status("✗ Download failed", "#ff4444")
            self.progress_bar['value'] = 0
            messagebox.showerror("Error", error_msg)
        finally:
            self.is_downloading = False
            self.download_btn.config(
                state="normal",
                text="⬇ START",
                bg=self.colors['button']
            )
    
    def start_download(self):
        if self.is_downloading:
            return
            
        self.is_downloading = True
        self.download_btn.config(
            state="disabled",
            text="⏳ LOADING...",
            bg="#555555"
        )
        thread = threading.Thread(target=self.download_thread, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
