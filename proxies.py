#!/usr/bin/env python3
"""
Proxy management for Multi-Format Video and Audio Downloader

This module provides proxy management functionality for the downloader.
It includes a list of public proxies and functions to select and validate proxies.
"""

import random
import requests
import time
import threading
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('proxy_manager')

# List of public proxies (HTTP/HTTPS)
# These are example proxies and should be replaced with actual working proxies
# Format: protocol://ip:port
PUBLIC_PROXIES = [
    # HTTP proxies
    "http://203.24.108.172:80",
    "http://203.23.106.192:80",
    "http://203.30.189.46:80",
    "http://203.32.121.98:80",
    "http://203.23.104.29:80",
    
    # HTTPS proxies
    "https://203.24.108.172:443",
    "https://203.23.106.192:443",
    "https://203.30.189.46:443",
    "https://203.32.121.98:443",
    "https://203.23.104.29:443",
    
    # SOCKS proxies
    "socks5://203.24.108.172:1080",
    "socks5://203.23.106.192:1080",
    "socks5://203.30.189.46:1080",
    "socks5://203.32.121.98:1080",
    "socks5://203.23.104.29:1080"
]

# Cache for working proxies
WORKING_PROXIES = []
LAST_PROXY_CHECK = 0
PROXY_CHECK_INTERVAL = 3600  # 1 hour in seconds
PROXY_LOCK = threading.Lock()

def is_youtube_url(url):
    """Check if the URL is from YouTube."""
    parsed_url = urlparse(url)
    return parsed_url.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be', 'm.youtube.com']

def test_proxy(proxy, timeout=5):
    """Test if a proxy is working."""
    try:
        response = requests.get('https://www.google.com', 
                               proxies={'http': proxy, 'https': proxy}, 
                               timeout=timeout)
        return response.status_code == 200
    except:
        return False

def update_working_proxies():
    """Update the list of working proxies."""
    global WORKING_PROXIES, LAST_PROXY_CHECK
    
    with PROXY_LOCK:
        current_time = time.time()
        # Only update if it's been more than PROXY_CHECK_INTERVAL since last check
        if current_time - LAST_PROXY_CHECK < PROXY_CHECK_INTERVAL and WORKING_PROXIES:
            return
        
        logger.info("Updating working proxies list...")
        WORKING_PROXIES = []
        
        for proxy in PUBLIC_PROXIES:
            if test_proxy(proxy):
                WORKING_PROXIES.append(proxy)
                logger.info(f"Proxy {proxy} is working")
        
        LAST_PROXY_CHECK = current_time
        logger.info(f"Found {len(WORKING_PROXIES)} working proxies")

def get_random_proxy(url=None):
    """Get a random working proxy. If url is provided, only return a proxy if it's a YouTube URL."""
    if url and not is_youtube_url(url):
        return None
    
    # Update working proxies if needed
    if not WORKING_PROXIES:
        update_working_proxies()
    
    # If we still don't have working proxies, return None
    if not WORKING_PROXIES:
        logger.warning("No working proxies available")
        return None
    
    # Return a random working proxy
    proxy = random.choice(WORKING_PROXIES)
    logger.info(f"Selected proxy: {proxy}")
    return proxy

# Initialize working proxies in a separate thread
def init_proxies():
    """Initialize the working proxies list in a background thread."""
    threading.Thread(target=update_working_proxies, daemon=True).start()

# Initialize proxies when module is imported
init_proxies()