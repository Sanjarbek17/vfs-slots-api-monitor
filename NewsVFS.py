#!/usr/bin/env python
"""
NewsVFS - VFS Global News Monitor

This module monitors the VFS Global news feed for updates.
It periodically checks for new articles and notifications,
sending desktop notifications when new content is detected.

Dependencies:
    - requests
    - pygame (for sound notifications)
"""

import os
import sys
import time
import json
import requests
import subprocess
import pygame
from urllib.parse import urlencode, quote_plus
from datetime import datetime


class NewsVFS:
    """
    A class to monitor and notify about VFS Global news updates.

    This class continuously monitors the VFS news API for new articles
    and sends desktop notifications when updates are detected.
    """

    def __init__(self, params):
        """
        Initialize the NewsVFS monitor.

        Args:
            params (dict): Configuration parameters including:
                - url: Base URL for the VFS news API
                - headers: HTTP headers for API requests
                - delay: Time between checks in seconds
                - max_num: Threshold for total news count
                - sound: Path to sound file for notifications
        """
        self.params = params

    def send_notification(self, title, message):
        """
        Send a desktop notification using the system's native notification system.

        Args:
            title (str): The notification title
            message (str): The notification message body

        Note:
            Uses osascript on macOS and notify-send on Linux
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

    def get_response(self, params):
        """
        Make an HTTP GET request to the VFS news API.

        Args:
            params (dict): Request parameters including:
                - url: The API endpoint URL
                - headers: HTTP headers for the request

        Returns:
            dict: The JSON response if successful
            False: If the request fails or returns non-200 status
        """
        resp = requests.get(params["url"], headers=params["headers"])
        if not 200 == resp.status_code:
            return False

        try:
            resp = resp.json()
        except ValueError as e:
            return False

        return resp

    def get_total(self, resp, key):
        """
        Extract the total count from the API response.

        Args:
            resp (dict): The API response dictionary
            key (str): The key containing the total count

        Returns:
            int: The total count if found
            False: If the key doesn't exist
        """
        if key in resp:
            return resp[key]
        return False

    def check_by_total(self, resp, key, current, post_date):
        """
        Check if there are new articles by comparing totals.

        Args:
            resp (dict): The API response dictionary
            key (str): The key to check in the response
            current (int): Current total count
            post_date (str): Date of the last post

        Returns:
            int: New total count if found
            False: If the key doesn't exist
        """
        if key in resp:
            return resp[key]
        return False

    def intialize(self):
        """
        Initialize and run the news monitoring loop.

        This method:
        - Displays the VFS ASCII art banner
        - Continuously monitors the news API
        - Sends notifications for new articles
        - Plays a sound alert when updates are found
        - Prints article details to the console
        """
        print(
            """
██    ██ ███████ ███████     ███    ██ ███████ ██     ██ ███████          
██    ██ ██      ██          ████   ██ ██      ██     ██ ██               
██    ██ █████   ███████     ██ ██  ██ █████   ██  █  ██ ███████          
 ██  ██  ██           ██     ██  ██ ██ ██      ██ ███ ██      ██          
  ████   ██      ███████     ██   ████ ███████  ███ ███  ███████ ██ ██ ██"""
        )
        print("\n")
        print("Watching VFS news API for update...")
        print("\n")

        count = 0
        while True:
            # Putting the script to sleep for the delay
            count += 1
            resp = self.get_response(self.params)

            print(".", end="", flush=True),

            if False == resp:
                continue

            total = self.get_total(resp, "total")
            if total > self.params["max_num"]:
                break
            time.sleep(self.params["delay"])

        print("\n")
        print("The total news count is", end=": ")
        print(total)

        self.send_notification(
            "VFS Notice Update!", "New article published at VFS notice board."
        )
        print("\n")
        for i in resp["items"]:
            print("-", end=" ")
            print(i["fields"]["date"], end=" --- ")
            print(i["fields"]["body"]["content"][0]["content"][0]["value"])
            print(">>", end=" ")
            print(i["fields"]["body"]["content"][1]["content"][0]["value"])
            print("\n")
        pygame.mixer.init()
        pygame.mixer.music.load(self.params["sound"])
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()


def main(params):
    """
    Main entry point for the VFS news monitor.

    Args:
        params (str): Path to the JSON configuration file

    Returns:
        False: If the configuration file doesn't exist
        None: When monitoring is complete or interrupted

    The configuration file should contain:
        - url: Base URL for the VFS news API
        - urlparams: Query parameters for the API
        - headers: HTTP headers for requests
        - delay: Time between checks
        - max_num: Threshold for total news count
        - sound: Path to notification sound file
    """
    if not os.path.isfile(params):
        return False

    path = os.path.realpath(params)
    read = open(path, "r")
    params = json.loads(read.read())
    read.close()

    params["url"] = (
        params["url"] + "?" + urlencode(params["urlparams"], quote_via=quote_plus)
    )

    resp = NewsVFS(params)
    resp.intialize()


if __name__ == "__main__":
    main("./news_creds.json")
