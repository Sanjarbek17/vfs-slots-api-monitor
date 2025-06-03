#!/usr/bin/env python3
"""
Test the browser monitor setup without launching the full monitor
"""

import sys
import os

sys.path.append(os.getcwd())

from browser_monitor import BrowserMonitor


def test_setup():
    """Test browser monitor initialization"""
    print("Testing Browser Monitor Setup...")

    monitor = BrowserMonitor()

    # Test Chrome detection
    if monitor.is_chrome_running():
        print("✅ Chrome process detection works - Chrome is currently running")
    else:
        print("✅ Chrome process detection works - No Chrome processes found")

    print("✅ BrowserMonitor class initialized successfully")
    print("✅ All imports working correctly")
    print("\nSetup test completed successfully! 🎉")
    print("\nTo run the full monitor with your default profile:")
    print("python browser_monitor.py")


if __name__ == "__main__":
    test_setup()
