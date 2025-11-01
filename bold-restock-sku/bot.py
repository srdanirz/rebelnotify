import requests
import json
import logging
import bcolors
import threading
import colorama
import random
import time

from datetime import datetime
from bs4 import BeautifulSoup
from _utils import proxy_config
from discord_webhook import DiscordEmbed, DiscordWebhook

notified_pids = []
pid_lock = threading.Lock()
size_code_tree = {
            "7": "070",
            "7.5": "075",
            "8": "080",
            "8.5": "085",
            "9": "090",
            "9.5": "095",
            "10": "100",
            "10.5": "105",
            "11": "110",
            "11.5": "115",
            "12": "120",
            "12.5": "125",
            "13": "130",
        }

colorama.init()

script_name = "Bold Monitor"


class Monitor:
    def __init__(self, bot_pid, task_number, proxy):
        

        # General
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        self.s = requests.session()
        self.task_number = task_number
        self.logger = logging.getLogger(str(task_number))
        self.logger.setLevel(logging.INFO)

        # Bold
        parsed_bot_pid = bot_pid.split(":")
        self.size = parsed_bot_pid[1]
        self.pid = parsed_bot_pid[0]
        self.size_pid = self.pid + size_code_tree.get(self.size)

        self.product_page = f"https://bold.cl/p/{self.size_pid}"
        self.product_name = self.size_pid
        self.product_image = None

        self.proxy = {} if localhost else proxy_config(proxy)
        self.csrf_token = None

    def __repr__(self):
        return f"Monitor(size={self.size}, pid={self.pid})"

    def log(self, text, status):
        if log_mode:
            self.logger.info(text)

        color_schemes = {
            "s": bcolors.OK,
            "f": bcolors.ERR,
            "p": bcolors.BLUE,
            "d": bcolors.WARN
        }
        color = color_schemes.get(status)
        # Special Loggings
        if status == "S":
            print(
                bcolors.OK + f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number}] - [{script_name}] - ({self.product_name}) - " + bcolors.OKMSG + f"{text}" + bcolors.ENDC)
            return
        if status == "F":
            print(
                bcolors.ERR + f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number}] - [{script_name}] - ({self.product_name}) - " + bcolors.ERRMSG + f"{text}" + bcolors.ENDC)
            return

        # Regular loggings
        print(color +
              f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - "
              f"[{self.task_number}] - "
              f"[{script_name}] - "
              f"({self.product_name}) - "
              f"{text}" + bcolors.ENDC
              )
    def __str__(self):
        return f"Bold Monitor for size {self.size} and PID {self.pid}"

    def log_request(self, request: requests.Response):
        if log_mode:
            log_object = {
                "path": request.request.path_url,
                "request_data": {
                    "request": {
                        "url": request.request.url,
                        "body": request.request.body,
                        "headers": request.request.headers,
                    },
                    "response": {
                        "url": request.url,
                        "body": request.text,
                        "headers": request.headers,
                    },
                    "cookies": request.cookies.get_dict()
                }
            }
            self.logger.debug(log_object)

    def send_webhook(self):
        color = 3066993
        webhook = DiscordWebhook(url=webhook_url)

        # create embed object for webhook
        embed = DiscordEmbed(title=f"In Stock Alert ({self.product_name})", color=color)

        # set footer
        embed.set_footer(text='Rebel Notify Bold Monitor')

        # set timestamp (default is now)
        embed.set_timestamp()
        embed.set_thumbnail(url="https://bold.cl" + self.product_image)
        # add fields to embed
        embed.add_embed_field(name="PID", value=self.pid)
        embed.add_embed_field(name="Size", value=f"[{self.size}]({self.product_page})")

        # add embed object to webhook
        webhook.add_embed(embed)

        webhook.execute()

    def rotate_proxy(self):
        self.proxy = random.choice(proxies)
        self.proxy = proxy_config(self.proxy)

    def start_session(self):
        self.log("Starting session...", "p")
        while True:
            productPageGET = self.s.get(
                self.product_page,
                headers={
                    "upgrade-insecure-requests": "1",
                    "user-agent": self.user_agent,
                },
                proxies=self.proxy
            )
            self.log_request(productPageGET)

            productPageHTML = BeautifulSoup(productPageGET.text, "html.parser")
            try:
                self.csrf_token = productPageGET.text.split("CSRFToken = '")[1].split("'")[0]
                self.product_image = productPageHTML.find("img", {"class": "custom-img"}).get("data-src")
            except IndexError:
                self.log(f"Product page not found.", "f")
                time.sleep(3)
                continue
            print(productPageHTML)
            break

    def empty_cart(self):
        self.log("Emptying cart...", "p")
        emptyCartPOST = self.s.post(
            "https://bold.cl/cart/entry/execute/REMOVE",
            data={
                "CSRFToken": self.csrf_token,
                "entryNumbers": 0
            },
            headers={
                "origin": "https://bold.cl",
                "referer": "https://bold.cl/cart",
                "upgrade-insecure-requests": "1",
                "user-agent": self.user_agent
            },
            proxies=self.proxy
        )

    def monitor(self):
        while True:
            addToCartPOST = self.s.post(
                "https://bold.cl/cart/add",
                data={
                    "qty": 1,
                    "productCodePost": self.size_pid,
                    "CSRFToken": self.csrf_token
                },
                headers={
                    "origin": "https://bold.cl",
                    "referer": self.product_page,
                    "upgrade-insecure-requests": "1",
                    "user-agent": self.user_agent
                },
                proxies=self.proxy
            )
            # Product not available
            if addToCartPOST.status_code in [404, 500]:
                self.log("Product is not available. Monitoring...", "f")
                time.sleep(3)
                continue

            # Unexpected error
            if addToCartPOST.status_code not in [200, 404, 500]:
                self.log(f"Failed to collect sizes ({addToCartPOST.status_code}). Retrying...", "f")
                self.log_request(addToCartPOST)
                self.rotate_proxy()
                time.sleep(3)
                continue

            self.product_name = addToCartPOST.json()['cartAnalyticsData'].get("productName")

            # Not carted
            if not addToCartPOST.json()['cartAnalyticsData'].get("cartCode"):
                self.log("Size not available.", "f")
                time.sleep(3)
                continue

            # Carted (available)
            self.log("Size available.", "S")
            self.empty_cart()
            if self.size_pid in notified_pids:
                self.log("Already notified recently. Sleeping...", "p")
                time.sleep(30)
                continue

            pid_lock.acquire()
            notified_pids.append(self.size_pid)
            pid_lock.release()

            self.send_webhook()

            # Timeout for 30 seconds before monitoring again.
            self.log("Sleeping...", "p")
            time.sleep(30)
            self.log("Done sleeping. Removing pid from notified list...", "p")
            pid_lock.acquire()
            notified_pids.remove(self.size_pid)
            pid_lock.release()

    def Bold(self):
        self.start_session()
        self.monitor()


if __name__ == '__main__':
    try:

        with open("settings.json", "r") as f:
            settings_file = json.load(f)

        with open("proxies.txt", "r") as f:
            proxies = [_proxy.replace("\n", "") for _proxy in f.readlines()]

        with open("pids.txt", "r") as f:
            pids = [_pid.replace("\n", "") for _pid in f.readlines()]

        webhook_url = settings_file["webhook_url"]
        log_mode = settings_file["log_mode"]
        localhost = settings_file['localhost']

        # Set up logger
        logFileName = datetime.now().strftime("%m-%d-%y %H_%M_%S")
        logging.basicConfig(
            filename=f"logs/{logFileName}.txt",
            format="%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s",
            filemode="w"
        )

        if localhost:
            assert len(pids) <= len(proxies), "Not enough proxies for pids."

        for taskNumber in range(len(pids)):

            monitor_instance = Monitor(
                bot_pid=pids[taskNumber],
                proxy=proxies[taskNumber],
                task_number=taskNumber + 1
            )
            threading.Thread(target=monitor_instance.Bold, args=()).start()
            time.sleep(2)

    except Exception as exc:
        logging.getLogger("STARTUP").exception("Failed to startup.")
        raise exc
