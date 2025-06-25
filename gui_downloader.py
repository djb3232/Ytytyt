#!/usr/bin/env python3
"""
GUI Multi-Format Video and Audio Downloader

A graphical interface for downloading videos and audio from various platforms in different formats.
Uses yt-dlp, a powerful fork of youtube-dl with additional features.
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil

class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Format Downloader")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Check dependencies
        self.check_dependencies()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL input
        ttk.Label(main_frame, text="URL(s) - One per line:").pack(anchor=tk.W, pady=(0, 5))
        self.url_text = tk.Text(main_frame, height=5)
        self.url_text.pack(fill=tk.X, pady=(0, 10))
        
        # Create frames for options
        options_frame = ttk.LabelFrame(main_frame, text="Download Options")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Format options
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(format_frame, text="Format:").grid(row=0, column=0, sticky=tk.W)
        self.format_var = tk.StringVar()
        format_options = ["Auto", "mp4", "webm", "mkv", "mp3", "m4a", "opus", "wav", "flac"]
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, values=format_options, width=10)
        self.format_combo.current(0)
        self.format_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(format_frame, text="Quality:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.quality_var = tk.StringVar()
        quality_options = ["Best", "1080", "720", "480", "360", "Worst"]
        self.quality_combo = ttk.Combobox(format_frame, textvariable=self.quality_var, values=quality_options, width=10)
        self.quality_combo.current(0)
        self.quality_combo.grid(row=0, column=3, padx=5)
        
        # Audio only option
        self.audio_only_var = tk.BooleanVar()
        ttk.Checkbutton(format_frame, text="Audio Only", variable=self.audio_only_var).grid(row=0, column=4, padx=(10, 0))
        
        # Playlist option
        self.playlist_var = tk.BooleanVar()
        ttk.Checkbutton(format_frame, text="Download Playlist", variable=self.playlist_var).grid(row=0, column=5, padx=(10, 0))
        
        # Subtitles
        subtitle_frame = ttk.Frame(options_frame)
        subtitle_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(subtitle_frame, text="Subtitles (comma separated language codes, e.g., en,fr):").grid(row=0, column=0, sticky=tk.W)
        self.subtitles_var = tk.StringVar()
        self.subtitles_entry = ttk.Entry(subtitle_frame, textvariable=self.subtitles_var)
        self.subtitles_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        subtitle_frame.columnconfigure(1, weight=1)
        
        # Output directory
        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W)
        self.output_dir_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.output_dir_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        self.output_dir_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=2, padx=5)
        output_frame.columnconfigure(1, weight=1)
        
        # Advanced options
        advanced_frame = ttk.LabelFrame(main_frame, text="Advanced Options")
        advanced_frame.pack(fill=tk.X, pady=10)
        
        # Proxy
        proxy_frame = ttk.Frame(advanced_frame)
        proxy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(proxy_frame, text="Proxy URL:").grid(row=0, column=0, sticky=tk.W)
        self.proxy_var = tk.StringVar()
        self.proxy_entry = ttk.Entry(proxy_frame, textvariable=self.proxy_var)
        self.proxy_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        proxy_frame.columnconfigure(1, weight=1)
        
        # Rate limit
        rate_frame = ttk.Frame(advanced_frame)
        rate_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(rate_frame, text="Rate Limit (e.g., 500K, 2M):").grid(row=0, column=0, sticky=tk.W)
        self.rate_var = tk.StringVar()
        self.rate_entry = ttk.Entry(rate_frame, textvariable=self.rate_var)
        self.rate_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        rate_frame.columnconfigure(1, weight=1)
        
        # Additional options
        options_frame2 = ttk.Frame(advanced_frame)
        options_frame2.pack(fill=tk.X, padx=10, pady=5)
        
        self.no_mtime_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame2, text="Don't use Last-modified header for file time", variable=self.no_mtime_var).pack(anchor=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="List Formats", command=self.list_formats).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Info", command=self.show_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Download", command=self.download).pack(side=tk.RIGHT, padx=5)
        
        # Output console
        console_frame = ttk.LabelFrame(main_frame, text="Console Output")
        console_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.console = tk.Text(console_frame, height=10, wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.console.config(state=tk.DISABLED)
        
        # Scrollbar for console
        scrollbar = ttk.Scrollbar(self.console, command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.config(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set focus to URL entry
        self.url_text.focus_set()
    
    def check_dependencies(self):
        """Check if yt-dlp is installed, if not, install it."""
        if shutil.which('yt-dlp') is None:
            self.update_console("yt-dlp not found. Installing...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yt-dlp'])
                self.update_console("yt-dlp installed successfully.")
            except subprocess.CalledProcessError:
                self.update_console("Failed to install yt-dlp. Please install it manually.")
                messagebox.showerror("Dependency Error", "Failed to install yt-dlp. Please install it manually.")
    
    def update_console(self, text):
        """Update the console with text."""
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def browse_output_dir(self):
        """Open a directory browser dialog."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def get_urls(self):
        """Get URLs from the text box."""
        urls_text = self.url_text.get("1.0", tk.END).strip()
        if not urls_text:
            messagebox.showerror("Error", "Please enter at least one URL.")
            return None
        return [url.strip() for url in urls_text.split("\n") if url.strip()]
    
    def build_command(self, action=None):
        """Build the yt-dlp command based on the GUI options."""
        urls = self.get_urls()
        if not urls:
            return None
        
        cmd = ['yt-dlp']
        
        # Handle format and quality
        format_val = self.format_var.get()
        quality_val = self.quality_var.get().lower()
        
        if self.audio_only_var.get():
            if format_val != "Auto" and format_val in ['mp3', 'm4a', 'opus', 'wav', 'flac']:
                cmd.extend(['-x', '--audio-format', format_val])
            else:
                cmd.extend(['-x', '--audio-format', 'mp3'])  # Default to mp3
        elif format_val != "Auto":
            if quality_val in ['best', 'worst']:
                quality_prefix = 'b' if quality_val == 'best' else 'w'
                cmd.extend(['-f', f'{quality_prefix}v[ext={format_val}]+{quality_prefix}a'])
            else:
                # For numeric quality like 1080, 720, etc.
                cmd.extend(['-f', f'bestvideo[height<={quality_val}][ext={format_val}]+bestaudio'])
        elif quality_val not in ['best', 'worst']:
            # For numeric quality like 1080, 720, etc.
            cmd.extend(['-f', f'bestvideo[height<={quality_val}]+bestaudio'])
        
        # Handle output directory
        output_dir = self.output_dir_var.get()
        if output_dir:
            cmd.extend(['-o', os.path.join(output_dir, '%(title)s.%(ext)s')])
        
        # Handle playlist
        if not self.playlist_var.get():
            cmd.append('--no-playlist')
        
        # Handle subtitles
        subtitles = self.subtitles_var.get().strip()
        if subtitles:
            cmd.extend(['--write-sub', '--sub-langs', subtitles])
        
        # Handle action-specific options
        if action == 'list':
            cmd.append('--list-formats')
        elif action == 'info':
            cmd.append('--dump-json')
        
        # Handle proxy
        proxy = self.proxy_var.get().strip()
        if proxy:
            cmd.extend(['--proxy', proxy])
        
        # Handle rate limit
        rate = self.rate_var.get().strip()
        if rate:
            cmd.extend(['--limit-rate', rate])
        
        # Handle mtime
        if self.no_mtime_var.get():
            cmd.append('--no-mtime')
        
        # Add URLs
        cmd.extend(urls)
        
        return cmd
    
    def run_command(self, cmd, action=None):
        """Run the command in a separate thread."""
        self.update_console(f"Executing: {' '.join(cmd)}")
        self.status_var.set("Running...")
        
        def target():
            try:
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                for line in process.stdout:
                    self.update_console(line.strip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.update_console("Command completed successfully.")
                    self.status_var.set("Completed")
                else:
                    self.update_console(f"Command failed with return code {process.returncode}")
                    self.status_var.set("Failed")
            except Exception as e:
                self.update_console(f"Error: {str(e)}")
                self.status_var.set("Error")
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
    
    def list_formats(self):
        """List available formats for the URL."""
        cmd = self.build_command(action='list')
        if cmd:
            self.run_command(cmd)
    
    def show_info(self):
        """Show information about the URL."""
        cmd = self.build_command(action='info')
        if cmd:
            self.run_command(cmd)
    
    def download(self):
        """Download the URL with the specified options."""
        cmd = self.build_command()
        if cmd:
            self.run_command(cmd)

def main():
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()