#!/usr/bin/env python3
"""
Test script to verify Python is working correctly on the server.
"""
import sys
import os

def main():
    """Print system information for debugging."""
    print("Content-Type: text/plain\n")
    print("Python Test Script")
    print("=================")
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Script Directory: {os.path.dirname(os.path.abspath(__file__))}")
    print("\nEnvironment Variables:")
    for key, value in sorted(os.environ.items()):
        print(f"  {key}: {value}")
    print("\nInstalled Packages:")
    try:
        import pkg_resources
        for pkg in sorted([f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]):
            print(f"  {pkg}")
    except ImportError:
        print("  pkg_resources not available")

if __name__ == "__main__":
    main()
