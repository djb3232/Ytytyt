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
        
        # Cookie options
        cookie_frame = ttk.LabelFrame(advanced_frame, text="Cookie Options (for restricted sites)")
        cookie_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Cookies file
        cookies_file_frame = ttk.Frame(cookie_frame)
        cookies_file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cookies_file_frame, text="Cookies File:").grid(row=0, column=0, sticky=tk.W)
        self.cookies_file_var = tk.StringVar()
        self.cookies_file_entry = ttk.Entry(cookies_file_frame, textvariable=self.cookies_file_var)
        self.cookies_file_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        ttk.Button(cookies_file_frame, text="Browse", command=self.browse_cookies_file).grid(row=0, column=2, padx=5)
        cookies_file_frame.columnconfigure(1, weight=1)
        
        # Browser cookies
        browser_cookies_frame = ttk.Frame(cookie_frame)
        browser_cookies_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(browser_cookies_frame, text="Extract cookies from browser:").grid(row=0, column=0, sticky=tk.W)
        self.browser_cookies_var = tk.StringVar(value="none")
        browser_options = ["none", "chrome", "firefox", "safari", "edge", "opera"]
        self.browser_cookies_combo = ttk.Combobox(browser_cookies_frame, textvariable=self.browser_cookies_var, values=browser_options, width=10)
        self.browser_cookies_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        # HTTP headers
        headers_frame = ttk.LabelFrame(advanced_frame, text="HTTP Headers")
        headers_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # User agent
        user_agent_frame = ttk.Frame(headers_frame)
        user_agent_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(user_agent_frame, text="User Agent:").grid(row=0, column=0, sticky=tk.W)
        self.user_agent_var = tk.StringVar()
        self.user_agent_entry = ttk.Entry(user_agent_frame, textvariable=self.user_agent_var)
        self.user_agent_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        user_agent_frame.columnconfigure(1, weight=1)
        
        # Referer
        referer_frame = ttk.Frame(headers_frame)
        referer_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(referer_frame, text="Referer URL:").grid(row=0, column=0, sticky=tk.W)
        self.referer_var = tk.StringVar()
        self.referer_entry = ttk.Entry(referer_frame, textvariable=self.referer_var)
        self.referer_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        referer_frame.columnconfigure(1, weight=1)
        
        # Custom headers
        custom_headers_frame = ttk.Frame(headers_frame)
        custom_headers_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(custom_headers_frame, text="Custom Headers (JSON):").grid(row=0, column=0, sticky=tk.W)
        self.custom_headers_var = tk.StringVar()
        self.custom_headers_entry = ttk.Entry(custom_headers_frame, textvariable=self.custom_headers_var)
        self.custom_headers_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        custom_headers_frame.columnconfigure(1, weight=1)
        
        # OAuth Authentication
        oauth_frame = ttk.LabelFrame(advanced_frame, text="OAuth Authentication")
        oauth_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # OAuth token
        token_frame = ttk.Frame(oauth_frame)
        token_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(token_frame, text="OAuth Token:").grid(row=0, column=0, sticky=tk.W)
        self.auth_token_var = tk.StringVar()
        self.auth_token_entry = ttk.Entry(token_frame, textvariable=self.auth_token_var)
        self.auth_token_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        token_frame.columnconfigure(1, weight=1)
        
        # Token type
        token_type_frame = ttk.Frame(oauth_frame)
        token_type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(token_type_frame, text="Token Type:").grid(row=0, column=0, sticky=tk.W)
        self.auth_token_type_var = tk.StringVar(value="Bearer")
        token_type_options = ["Bearer", "Basic", "Digest", "OAuth"]
        self.auth_token_type_combo = ttk.Combobox(token_type_frame, textvariable=self.auth_token_type_var, values=token_type_options, width=10)
        self.auth_token_type_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
        
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
    
    def browse_cookies_file(self):
        """Open a file browser dialog for cookies file."""
        file_path = filedialog.askopenfilename(
            title="Select Cookies File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.cookies_file_var.set(file_path)
    
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
        
        # Handle cookies file
        cookies_file = self.cookies_file_var.get().strip()
        if cookies_file:
            cmd.extend(['--cookies', cookies_file])
        
        # Handle browser cookies
        browser_cookies = self.browser_cookies_var.get()
        if browser_cookies and browser_cookies != 'none':
            cmd.extend(['--cookies-from-browser', browser_cookies])
        
        # Handle user agent
        user_agent = self.user_agent_var.get().strip()
        if user_agent:
            cmd.extend(['--user-agent', user_agent])
        
        # Handle referer
        referer = self.referer_var.get().strip()
        if referer:
            cmd.extend(['--referer', referer])
        
        # Handle custom headers and OAuth token
        custom_headers = self.custom_headers_var.get().strip()
        auth_token = self.auth_token_var.get().strip()
        auth_token_type = self.auth_token_type_var.get()
        
        import json
        
        if auth_token:
            # Create Authorization header with the token
            auth_header = f'Authorization: {auth_token_type} {auth_token}'
            
            if custom_headers:
                try:
                    # Parse existing headers
                    headers_dict = json.loads(custom_headers)
                    # Add Authorization header
                    headers_dict['Authorization'] = f'{auth_token_type} {auth_token}'
                    # Convert back to JSON
                    cmd.extend(['--add-headers', json.dumps(headers_dict)])
                except (json.JSONDecodeError, ImportError):
                    # If not valid JSON, create a new headers dict
                    self.update_console("Warning: Invalid JSON format for custom headers. Creating new headers with OAuth token.")
                    headers_dict = {'Authorization': f'{auth_token_type} {auth_token}'}
                    cmd.extend(['--add-headers', json.dumps(headers_dict)])
            else:
                # No existing headers, just add the Authorization header
                headers_dict = {'Authorization': f'{auth_token_type} {auth_token}'}
                cmd.extend(['--add-headers', json.dumps(headers_dict)])
        elif custom_headers:
            try:
                # Validate JSON format
                json.loads(custom_headers)
                cmd.extend(['--add-headers', custom_headers])
            except (json.JSONDecodeError, ImportError):
                # If not valid JSON or json module not available, ignore
                self.update_console("Warning: Invalid JSON format for custom headers. Ignoring.")
        
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