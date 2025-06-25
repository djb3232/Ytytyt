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

# List of custom proxies (HTTP/HTTPS/SOCKS)
# Format: protocol://ip:port
PUBLIC_PROXIES = [
    # HTTP proxies
    "http://45.79.158.235:44554",
    "http://185.162.229.34:80",
    "http://103.152.112.162:80",
    "http://103.149.130.38:80",
    "http://103.118.40.119:80",
    
    # HTTPS proxies
    "https://103.83.232.122:80",
    "https://103.152.112.162:80",
    "https://185.162.229.34:80",
    "https://103.149.130.38:80",
    "https://103.118.40.119:80",
    
    # SOCKS proxies
    "socks5://72.221.232.155:4145",
    "socks5://72.195.34.35:27360",
    "socks5://72.217.216.239:4145",
    "socks5://72.210.252.134:46164",
    "socks5://72.206.181.97:64943",
    "socks5://72.195.114.169:4145",
    "socks5://72.195.34.42:4145",
    "socks5://72.210.208.101:4145",
    "socks5://72.221.172.203:4145",
    "socks5://72.206.181.103:4145"
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
        # Extract protocol from proxy string
        protocol = proxy.split('://')[0]
        
        # Test URL based on protocol
        if protocol == 'socks5':
            test_url = 'https://www.youtube.com'
        else:
            test_url = f"{protocol}://www.google.com"
        
        # Set up proxies dict based on protocol
        proxies = {protocol: proxy}
        if protocol == 'socks5':
            proxies = {'http': proxy, 'https': proxy}
        
        # Make request with proxy
        response = requests.get(test_url, 
                               proxies=proxies, 
                               timeout=timeout,
                               headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        
        return response.status_code == 200
    except Exception as e:
        logger.debug(f"Proxy {proxy} failed: {str(e)}")
        return False

def fetch_additional_proxies():
    """Fetch additional proxies from public APIs."""
    additional_proxies = []
    
    try:
        # Try to fetch HTTP proxies
        response = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all', 
                               timeout=10)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if line.strip():
                    additional_proxies.append(f"http://{line.strip()}")
        
        # Try to fetch SOCKS5 proxies
        response = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all', 
                               timeout=10)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if line.strip():
                    additional_proxies.append(f"socks5://{line.strip()}")
    
    except Exception as e:
        logger.warning(f"Failed to fetch additional proxies: {str(e)}")
    
    return additional_proxies

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
        
        # First test our custom proxies
        for proxy in PUBLIC_PROXIES:
            if test_proxy(proxy):
                WORKING_PROXIES.append(proxy)
                logger.info(f"Custom proxy {proxy} is working")
        
        # If we have fewer than 5 working proxies, try to fetch additional ones
        if len(WORKING_PROXIES) < 5:
            logger.info("Fetching additional proxies from public APIs...")
            additional_proxies = fetch_additional_proxies()
            logger.info(f"Fetched {len(additional_proxies)} additional proxies")
            
            # Test the additional proxies
            for proxy in additional_proxies:
                if len(WORKING_PROXIES) >= 10:  # Stop once we have 10 working proxies
                    break
                
                if test_proxy(proxy):
                    WORKING_PROXIES.append(proxy)
                    logger.info(f"Additional proxy {proxy} is working")
        
        LAST_PROXY_CHECK = current_time
        logger.info(f"Found {len(WORKING_PROXIES)} working proxies")

def get_random_proxy(url=None, protocol=None):
    """
    Get a random working proxy.
    
    Args:
        url (str, optional): If provided, only return a proxy if it's a YouTube URL.
        protocol (str, optional): If provided, only return a proxy with this protocol (http, https, socks5).
        
    Returns:
        str: A proxy URL or None if no suitable proxy is found.
    """
    if url and not is_youtube_url(url):
        return None
    
    # Update working proxies if needed
    if not WORKING_PROXIES:
        update_working_proxies()
    
    # If we still don't have working proxies, return None
    if not WORKING_PROXIES:
        logger.warning("No working proxies available")
        return None
    
    # Filter proxies by protocol if specified
    available_proxies = WORKING_PROXIES
    if protocol:
        available_proxies = [p for p in WORKING_PROXIES if p.startswith(f"{protocol}://")]
        if not available_proxies:
            logger.warning(f"No working {protocol} proxies available, using any protocol")
            available_proxies = WORKING_PROXIES
    
    # Return a random working proxy
    proxy = random.choice(available_proxies)
    logger.info(f"Selected proxy: {proxy}")
    return proxy

def get_best_proxy(url):
    """
    Get the best proxy for a specific URL based on response time.
    
    Args:
        url (str): The URL to test proxies against.
        
    Returns:
        str: The proxy with the fastest response time, or None if no working proxy is found.
    """
    if not is_youtube_url(url):
        return None
    
    # Update working proxies if needed
    if not WORKING_PROXIES:
        update_working_proxies()
    
    # If we still don't have working proxies, return None
    if not WORKING_PROXIES:
        logger.warning("No working proxies available")
        return None
    
    # Test each proxy against the URL and measure response time
    proxy_times = []
    for proxy in WORKING_PROXIES:
        try:
            start_time = time.time()
            protocol = proxy.split('://')[0]
            proxies = {protocol: proxy}
            if protocol == 'socks5':
                proxies = {'http': proxy, 'https': proxy}
            
            response = requests.head(url, 
                                   proxies=proxies, 
                                   timeout=5,
                                   headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            
            if response.status_code == 200:
                response_time = time.time() - start_time
                proxy_times.append((proxy, response_time))
                logger.info(f"Proxy {proxy} response time: {response_time:.2f}s")
        except Exception as e:
            logger.debug(f"Proxy {proxy} failed for URL {url}: {str(e)}")
    
    # Sort proxies by response time
    if proxy_times:
        proxy_times.sort(key=lambda x: x[1])
        best_proxy = proxy_times[0][0]
        logger.info(f"Best proxy for {url}: {best_proxy} ({proxy_times[0][1]:.2f}s)")
        return best_proxy
    
    # If no proxy worked, return a random one
    logger.warning(f"No proxy worked for {url}, returning random proxy")
    return get_random_proxy(url)

# Initialize working proxies in a separate thread
def init_proxies():
    """Initialize the working proxies list in a background thread."""
    threading.Thread(target=update_working_proxies, daemon=True).start()

# Initialize proxies when module is imported
init_proxies()