#!/usr/bin/env python
"""
AuthVFS - VFS Global Authentication Handler

This module handles the authentication process with VFS Global's website.
It automates the login process, manages CAPTCHA detection, and extracts
JWT tokens required for API access.

Dependencies:
    - undetected_chromedriver
    - selenium
"""

import os
import time
import json
from datetime import datetime
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthVFS:
    """
    A class to handle VFS Global authentication and JWT token management.

    This class automates the login process to VFS Global's website and
    extracts JWT tokens needed for API access. It handles CAPTCHA detection
    and provides automated retry mechanisms.
    """

    # default constructor
    def __init__(self, args, jwt):
        """
        Initialize the AuthVFS instance.

        Args:
            args (dict): Configuration parameters including:
                - url: Login page URL
                - user: Username/email
                - pass: Password
                - auth_path: Path to store JWT
                - avrg_delay: Average delay between actions
                - refr_delay: Refresh delay
            jwt (str): Initial JWT token (if any)
        """
        self.args = args
        self.jwt = jwt

    def create_driver(self):
        """
        Create and configure an undetected Chrome WebDriver instance.

        This method sets up a Chrome browser with specific options to:
        - Run in incognito mode
        - Use specific window size
        - Enable stability options
        - Configure for automation detection avoidance
        """
        options = uc.ChromeOptions()
        # Let's work in incognito mode.
        options.add_argument("--incognito")
        # Force Chrome to show up
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Initialize undetected-chromedriver
        self.driver = uc.Chrome(
            options=options,
            driver_executable_path=None,  # Will be automatically downloaded
            browser_executable_path=None,  # Will use default Chrome
            headless=False,  # Show the browser
            use_subprocess=True,  # More stable
            version_main=None,  # Will detect Chrome version
        )

    def get_loggedin(self, args, driver):
        """
        Handle the login process on the VFS website.

        Args:
            args (dict): Login credentials and selectors
            driver: Selenium WebDriver instance

        Returns:
            WebDriver: The driver instance after login attempt
            False: If login elements cannot be found

        This method:
        - Waits for login form elements to be present
        - Fills in credentials
        - Handles form submission
        - Reports progress via console
        """
        try:
            print("\nWaiting for login form to load...")
            # Wait up to 20 seconds for elements to be present
            wait = WebDriverWait(driver, 20)

            # Wait for each element with explicit waits
            email = wait.until(
                EC.presence_of_element_located((By.NAME, "email")),
                message="Email field not found",
            )
            print("Found email field")

            password = wait.until(
                EC.presence_of_element_located((By.NAME, "password")),
                message="Password field not found",
            )
            print("Found password field")

            submit = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")),
                message="Submit button not found or not clickable",
            )
            print("Found submit button")

            print("All form elements located successfully!")
        except Exception as e:
            print(f"\nError finding login elements: {str(e)}")
            return False

        # Fill up the form fields with necessary credentials.
        email.send_keys(args["user"])
        password.send_keys(args["pass"])
        time.sleep(self.args["avrg_delay"])
        # Submit the form.
        submit.click()
        # Wait 10 seconds for the response to come.
        time.sleep(self.args["avrg_delay"])
        # Return the driver instance.
        return driver

    def get_jwt(self, args):
        """
        Extract JWT token from the browser session.

        Args:
            args (dict): Configuration including URL and login info

        Returns:
            str: Valid JWT token if found and valid
            None: If no valid token can be obtained

        This method:
        - Checks current session for valid JWT
        - Handles navigation to login page if needed
        - Manages CAPTCHA detection
        - Retries on failure with appropriate delays
        """
        driver = self.driver
        while True:
            try:
                current_url = driver.current_url
                if "login" not in current_url:
                    # If we're not on the login page, try to get JWT first
                    try:
                        jwt = driver.execute_script("return window.sessionStorage.JWT")
                        if isinstance(jwt, str) and len(jwt) > 10:
                            return jwt
                    except:
                        pass

                # Only navigate to login if necessary
                if "login" not in current_url:
                    driver.get(args["url"])
                    time.sleep(self.args["avrg_delay"])  # Wait for page load
            except:
                time.sleep(self.args["avrg_delay"])
                continue

            # Try to login only if we're on the login page
            if "login" in driver.current_url:
                driver = self.get_loggedin(args, driver)
                time.sleep(self.args["avrg_delay"])  # Wait after login attempt

            try:
                # Check if we're on a CAPTCHA page
                if (
                    "are-you-human" in driver.current_url
                    or "recaptcha" in driver.page_source.lower()
                ):
                    print(
                        "\nCAPTCHA detected! Please solve the CAPTCHA in the browser window..."
                    )
                    time.sleep(self.args["avrg_delay"])
                    continue

                # Check if login was successful
                driver.find_element("xpath", args["ensure_login"])
                jwt = driver.execute_script("return window.sessionStorage.JWT")
                if isinstance(jwt, str) and len(jwt) > 10:
                    print("\nLogin successful!")
                    return jwt
            except:
                # If we couldn't find the success element or JWT, wait before retrying
                time.sleep(self.args["avrg_delay"])
                continue

            if isinstance(jwt, str) and 10 < len(jwt):
                return jwt

    def write_auth(self, file_path, jwt):
        """
        Write JWT token to a file.

        Args:
            file_path (str): Path to store the JWT token
            jwt (str): The JWT token to store

        Returns:
            bool: True if token was written successfully,
                 False if token is invalid or write fails

        This method:
        - Removes existing token file if present
        - Validates token before writing
        - Creates new file with token
        """
        if os.path.exists(file_path):
            file_path = os.path.realpath(file_path)
            os.remove(file_path)

        f = open(file_path, "a")

        if not isinstance(jwt, str) or 10 > len(jwt):
            return False

        f.write(jwt)
        f.close()
        return True

    def intialize(self):
        """
        Initialize and run the authentication process.

        This method:
        - Creates a new browser instance
        - Displays startup banner
        - Continuously attempts to obtain and store JWT tokens
        - Handles delays between attempts
        - Provides visual feedback via console
        """
        self.create_driver()
        print(
            """
██    ██ ███████ ███████          ██ ██     ██ ████████
██    ██ ██      ██               ██ ██     ██    ██
██    ██ █████   ███████          ██ ██  █  ██    ██
 ██  ██  ██           ██     ██   ██ ██ ███ ██    ██
  ████   ██      ███████      █████   ███ ███     ██ ██ ██ ██"""
        )

        print("\n")
        print("Started at:", end=" ")
        print(datetime.now())
        print("Generating JWT for VFS slots API...")
        print("\n")

        count = 0
        while True:
            jwt = self.get_jwt(self.args)
            if self.write_auth(self.args["auth_path"], jwt):
                count += 1
                # # Printing the JWT, Time and Count
                # print("JWT:", end =" ")
                # print(jwt)
                # print("Time:", end =" ")
                # print(datetime.now(), end =" --- Count: ")
                # print(count)
                # print("====")
                print(".", end="", flush=True),
                # Putting the script to sleep for the delay
                time.sleep(self.args["refr_delay"])


def main(params):
    """
    Main entry point for the VFS authentication script.

    Args:
        params (str): Path to JSON configuration file

    The configuration file should contain:
        - url: VFS login page URL
        - user: Username/email
        - pass: Password
        - auth_path: Path to store JWT
        - avrg_delay: Average delay between actions
        - refr_delay: Refresh delay
        - ensure_login: XPath to verify successful login
    """
    params = open(params, "r")
    params = json.loads(params.read())
    # creating object of the class
    auth = AuthVFS(params, "")
    auth.intialize()


if __name__ == "__main__":
    main("./auth_creds.json")
