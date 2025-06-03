#!/usr/bin/env python3
"""
VFS Global Access Test
Quick test to see which method bypasses VFS Global blocking
"""

import subprocess
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def test_stealth_selenium():
    """Test stealth Selenium approach"""
    print("🧪 Testing Stealth Selenium approach...")
    try:
        chrome_options = Options()

        # Maximum stealth options
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Apply stealth scripts
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        # Test VFS Global access
        driver.get("https://visa.vfsglobal.com/uzb/en/ltp/login/")
        time.sleep(3)

        title = driver.title
        url = driver.current_url

        driver.quit()

        if "blocked" in title.lower() or "error" in url.lower():
            print("❌ Stealth Selenium: BLOCKED")
            return False
        else:
            print(f"✅ Stealth Selenium: SUCCESS - {title}")
            return True

    except Exception as e:
        print(f"❌ Stealth Selenium: ERROR - {e}")
        return False


def test_remote_debugging():
    """Test remote debugging approach"""
    print("🧪 Testing Remote Debugging approach...")
    try:
        # Kill existing Chrome
        subprocess.run(["pkill", "-f", "Google Chrome"], capture_output=True)
        time.sleep(2)

        # Start Chrome with remote debugging
        import tempfile

        temp_profile = tempfile.mkdtemp(prefix="test_chrome_")

        chrome_cmd = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--remote-debugging-port=9222",
            f"--user-data-dir={temp_profile}",
            "--no-first-run",
            "--headless",  # Run headless for testing
        ]

        chrome_process = subprocess.Popen(
            chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        time.sleep(3)

        # Test remote debugging connection
        response = requests.get("http://127.0.0.1:9222/json/version", timeout=5)
        if response.status_code != 200:
            raise Exception("Remote debugging not available")

        # Connect Selenium
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        driver = webdriver.Chrome(options=chrome_options)

        # Test VFS Global access
        driver.get("https://visa.vfsglobal.com/uzb/en/ltp/login/")
        time.sleep(3)

        title = driver.title
        url = driver.current_url

        driver.quit()
        chrome_process.terminate()

        if "blocked" in title.lower() or "error" in url.lower():
            print("❌ Remote Debugging: BLOCKED")
            return False
        else:
            print(f"✅ Remote Debugging: SUCCESS - {title}")
            return True

    except Exception as e:
        print(f"❌ Remote Debugging: ERROR - {e}")
        return False


def main():
    print("🔍 VFS Global Access Test")
    print("Testing different approaches to bypass VFS Global blocking...")
    print("=" * 60)

    # Test both approaches
    stealth_works = test_stealth_selenium()
    remote_works = test_remote_debugging()

    print("\n" + "=" * 60)
    print("📊 RESULTS:")

    if remote_works:
        print("🏆 RECOMMENDED: Use vfs_remote_monitor.py")
        print("   Remote debugging is the most reliable method")
    elif stealth_works:
        print("🥈 RECOMMENDED: Use vfs_stealth_monitor.py")
        print("   Stealth Selenium should work")
    else:
        print(
            "⚠️  Both methods were blocked. VFS Global may have updated their detection."
        )
        print("   Try running the monitors manually for better results.")

    print("\n💡 Next steps:")
    if remote_works:
        print("   python3 vfs_remote_monitor.py")
    elif stealth_works:
        print("   python3 vfs_stealth_monitor.py")
    else:
        print("   Try manual browsing first to establish a session")


if __name__ == "__main__":
    main()
