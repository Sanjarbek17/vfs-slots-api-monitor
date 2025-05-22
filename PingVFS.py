#!/usr/bin/env python
"""
PingVFS - VFS Global Appointment Slot Monitor

This module continuously monitors the VFS Global appointment system API
for available slots. It uses JWT authentication and provides
notifications when slots become available.

Dependencies:
    - requests
    - pygame (for sound notifications)
    - urllib.parse (for URL handling)
"""

import os
import sys
import time
import json
import requests
import subprocess
import pygame
from urllib.parse import urlencode, quote_plus
from datetime import datetime, timedelta


class PingVFS:
    """
    A class to monitor VFS Global appointment slots availability.

    This class periodically checks the VFS appointment API for available
    slots, manages authentication, and provides notifications when
    slots are found.
    """

    # default constructor
    def __init__(self, params):
        """
        Initialize the PingVFS monitor.

        Args:
            params (dict): Configuration parameters including:
                - url: Base API URL
                - urlparams: URL query parameters
                - paths: Paths for auth and output files
                - sound: Path to alert sound file
        """
        self.url = params["url"]
        self.urlparams = params["urlparams"]
        self.paths = params["paths"]
        self.auth = ""
        self.start_time = datetime.now()
        self.sound = params["sound"]

    def get_auth_token(self):
        """
        Read and validate the authentication token.

        Returns:
            str: Valid authentication token
            False: If token file doesn't exist or is invalid

        This method:
        - Reads token from file
        - Validates token format
        - Caches token for subsequent use
        """
        if not os.path.isfile(self.paths["auth"]):
            return False

        path = os.path.realpath(self.paths["auth"])
        read = open(path, "r")
        auth = read.read().replace("\n", " ")
        read.close()

        if auth == self.auth:
            return self.auth

        self.auth = auth
        # os.remove(path)
        return self.auth

    def store_output(self, output):
        """
        Store API response output to a file.

        Args:
            output (str): The output text to store

        This method appends the output to the configured output file,
        creating a log of all API responses.
        """
        with open(self.paths["output"], "a") as file_object:
            file_object.write(output)

    def get_foramtted_date(self, date):
        """
        Format a date for the VFS API.

        Args:
            date (datetime.date): The date to format

        Returns:
            str: Date formatted as dd/mm/yyyy

        This method converts Python date objects to the
        format required by the VFS API.
        """
        return datetime.strptime(str(date), "%Y-%m-%d").strftime("%d/%m/%Y")

    def hit_vfs(self):
        """
        Make a request to the VFS appointment API.

        Returns:
            str: JSON response if successful
            str: Error message if request fails

        This method:
        - Constructs API request with authentication
        - Sets date range for appointment search
        - Handles connection and JSON parsing errors
        """
        headers = {
            "Content-length": "0",
            "Content-type": "application/json",
        }

        headers["Authorization"] = self.auth

        from_date = datetime.now().date() + timedelta(days=1)
        to_date = from_date + timedelta(days=90)

        self.urlparams["fromDate"] = str(self.get_foramtted_date(from_date))
        self.urlparams["toDate"] = str(self.get_foramtted_date(to_date))

        url = self.url + "?" + urlencode(self.urlparams, quote_via=quote_plus)

        try:
            resp = requests.get(url, headers=headers)
        except:
            return "ERROR Connection Refused"

        if os.path.isfile(self.paths["auth"]):
            self.get_auth_token()

        try:
            resp = resp.json()
        except:
            return "ERROR " + str(resp.status_code)

        return json.dumps(resp)

    def send_notification(self, title, message):
        """
        Send a desktop notification using the system's native notification system.

        Args:
            title (str): The notification title
            message (str): The notification message

        This method uses:
        - osascript for macOS notifications
        - notify-send for Linux notifications
        """
        if sys.platform == "darwin":  # macOS
            os.system(
                """
                osascript -e 'display notification "{}" with title "{}"'
            """.format(
                    message, title
                )
            )
        else:  # Linux
            subprocess.call(["/usr/bin/notify-send", title, message])

    def init(self):
        """
        Initialize and run the appointment slot monitoring process.

        This method:
        - Verifies authentication token
        - Displays startup banner
        - Continuously monitors the API for slots
        - Logs responses and tracks statistics
        - Sends notifications when slots are found
        - Plays sound alerts for immediate attention
        """
        auth = self.get_auth_token()
        count = 0

        print(
            """
██    ██ ███████ ███████     ███████ ██       ██████  ████████ ███████          
██    ██ ██      ██          ██      ██      ██    ██    ██    ██               
██    ██ █████   ███████     ███████ ██      ██    ██    ██    ███████          
 ██  ██  ██           ██          ██ ██      ██    ██    ██         ██          
  ████   ██      ███████     ███████ ███████  ██████     ██    ███████ ██ ██ ██"""
        )

        print("\n")
        print("Started at:", end=" ")
        print(datetime.now())
        print("Trying to access VFS appointment API for slots...")
        print("\n")

        while True:
            time.sleep(5)

            request = self.hit_vfs()
            count += 1

            output = (
                "\nOutput: "
                + str(request)
                + "\nTime: "
                + str(datetime.now())
                + "\nCount: "
                + str(count)
                + "\n==="
            )

            self.store_output(output)

            # Printing the output in terminal.
            # print(output)
            print(".", end="", flush=True),

            if request == "[[]]":
                continue
            try:
                request = json.loads(request)
            except:
                continue

            try:
                if request[0]["counters"] != None:
                    break
            except:
                continue

        self.send_notification("VFS Slots!!!", "Something Positive May Have Happened.")
        print("\n")
        print(str(count) + " times HTTP 200 response received.")
        print("Ended at:", end=" ")
        print(datetime.now())
        time_diff = datetime.now() - self.start_time
        time_diff = time_diff.total_seconds() / 60.0
        print("Script ran for " + str(time_diff) + " minutes")
        # Will play the alert sound.
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()


def main(params):
    """
    Main entry point for the VFS appointment slot monitor.

    Args:
        params (str): Path to JSON configuration file

    Returns:
        False: If configuration file doesn't exist

    The configuration file should contain:
        - url: Base API URL
        - urlparams: Query parameters
        - paths: File paths for auth and output
        - sound: Path to alert sound file
    """
    if not os.path.isfile(params):
        return False

    path = os.path.realpath(params)
    read = open(path, "r")
    params = json.loads(read.read())
    read.close()

    ping = PingVFS(params)
    ping.init()


if __name__ == "__main__":
    main("./ping_creds.json")
