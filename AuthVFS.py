#!/usr/bin/env python
import os
import time
import json
from datetime import datetime
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException


class AuthVFS:
    # default constructor
    def __init__(self, args, jwt):
        self.args = args
        self.jwt = jwt

    def create_driver(self):
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
        try:
            # Find the elements in the page.
            email = driver.find_element("xpath", args["email_id"])
            password = driver.find_element("xpath", args["password_id"])
            submit = driver.find_element("xpath", args["submit"])
        except NoSuchElementException:
            # If any of the elements aren"t there, return false.
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
        driver = self.driver
        while True:
            try:
                # Initiate the GET request.
                driver.get(args["url"])
            except:
                return False

            # Let the page load fully.
            time.sleep(self.args["avrg_delay"])  # Waitng 10 seconds.
            driver = self.get_loggedin(args, driver)

            try:
                driver.find_element("xpath", args["ensure_login"])
                jwt = driver.execute_script("return window.sessionStorage.JWT")
            except:
                continue

            if isinstance(jwt, str) and 10 < len(jwt):
                return jwt

    def write_auth(self, file_path, jwt):
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
    params = open(params, "r")
    params = json.loads(params.read())
    # creating object of the class
    auth = AuthVFS(params, "")
    auth.intialize()


if __name__ == "__main__":
    main("./auth_creds.json")
