#!/usr/bin/env python3
"""
Test script for Multi-Format Video and Audio Downloader

This script tests the basic functionality of the web application.
"""

import os
import sys
import requests
import time
import argparse

def test_web_app(url):
    """Test the web application."""
    print(f"Testing web application at {url}...")
    
    try:
        # Test home page
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Home page is accessible")
        else:
            print(f"❌ Home page returned status code {response.status_code}")
            return False
        
        # Check if the form is present
        if "Download" in response.text and "URL" in response.text:
            print("✅ Download form is present")
        else:
            print("❌ Download form not found")
            return False
        
        print("All tests passed! The application is working correctly.")
        return True
    
    except Exception as e:
        print(f"❌ Error testing web application: {e}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Test the Multi-Format Video and Audio Downloader web application')
    parser.add_argument('--url', default='http://localhost:12000', help='URL of the web application')
    
    args = parser.parse_args()
    
    success = test_web_app(args.url)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()