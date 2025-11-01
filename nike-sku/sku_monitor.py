import bcolors
import json
import threading
import colorama
import urllib3
import time
import helheim
import cloudscraper
import xmltodict
import argparse

from _utils import log
from termcolor import colored
from collections import OrderedDict
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests.adapters import HTTPAdapter, Retry
from json.decoder import JSONDecodeError

colorama.init()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
helheim.auth('e9efa3e3-d06f-4bbf-a7d6-e98e6fbdd2b3')

notified_skus = []


class Task:
    def __init__(self, sku, task_number, settings, proxy, taskLock, sessionLock, proxyLock):

        # IMPORTANT
        self.sku = sku
        self.item_data = None

        # General
        self.s = None
        self.task_number = task_number
        self.webhook_urls = settings["webhook_url"]
        self.fail_webhook_url = settings["fail_webhook_url"]
        self.proxy = proxy
        self.tls_proxy = None
        self.taskLock = taskLock
        self.sLock = sessionLock
        self.proxyLock = proxyLock
        self.delay = settings["delay"] / 1000
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"

        # Product
        self.product_name = None
        self.product_image = None
        self.product_url = None
        self.product_color = None
        self.product_sku = None
        self.size = None

    def proxy_config(self):
        parsed_proxy = None
        try:
            (IPv4, Port, username, password) = self.proxy.split(':')
            ip = IPv4 + ':' + Port
            parsed_proxy = {
                "http": "http://" + username + ":" + password + "@" + ip,
                "https": "http://" + username + ":" + password + "@" + ip,
            }
            self.tls_proxy = f"http://{username}:{password}@{ip}"
        except ValueError:
            self.log("Invalid proxy.", "f")
            exit(1)
        self.proxy = parsed_proxy

    @staticmethod
    def injection(session, response):
        if helheim.isChallenge(session, response):
            return helheim.solve(session, response)
        else:
            return response

    def log(self, text, status):
        if status == 's':
            print(colored(
                f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number + 1}] - {text}",
                'green'))
        if status == 'f':
            print(colored(
                f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number + 1}] - {text}",
                'red'))
        if status == 'p':
            print(colored(
                f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number + 1}] - {text}",
                'cyan'))

        if status == 'd':
            print(colored(
                f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number + 1}] - {text}",
                'yellow'))
        if status == "S":
            print(
                bcolors.OK + f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number + 1}] - " + bcolors.OKMSG + f"{text}" + bcolors.ENDC)

        if status == "F":
            print(
                bcolors.ERR + f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - [{self.task_number + 1}] - " + bcolors.ERRMSG + f"{text}" + bcolors.ENDC)

    def get_notified_skus(self):
        global notified_skus
        self.taskLock.acquire()
        returned = notified_skus
        self.taskLock.release()
        return returned

    def add_notified_sku(self):
        global notified_skus
        self.taskLock.acquire()
        notified_skus.append(self.sku)
        self.taskLock.release()

    def remove_notified_sku(self):
        global notified_skus
        self.taskLock.acquire()
        if self.sku in notified_skus:
            notified_skus.remove(self.sku)
        self.taskLock.release()

    def rotate_proxy(self):
        global proxies

        self.log("Rotating proxy...", "d")
        self.proxyLock.acquire()
        try:
            self.proxy = proxies[0]
            proxies.pop(0)
        except IndexError:
            self.log("No proxies to rotate to!", "F")
            self.send_webhook(True)
            self.proxyLock.release()
            exit(1)
        self.proxyLock.release()

    def handle(self, _request):

        try:
            json_response = _request.json()
        except JSONDecodeError:
            json_response = "None Found"

        if _request.status_code == 200 or _request.status_code == 201:
            return True
        elif _request.status_code == 403 or _request.status_code == 428:
            self.log(f"Access Denied. (Code {_request.status_code})", "f")
        elif _request.status_code == 404:
            self.log(f"Failed to find page. (Code 404, Request URL: {_request.request.url}, Response: {json_response})",
                     "f")
        elif _request.status_code == 500:
            self.log(
                f"Internal Server Error. Request was done incorrectly. (Code: 500, Request URL: {_request.request.url}, Response: {json_response})",
                "f")
        else:
            response = f"Unknown error occurred. (Code: {_request.status_code}, Request URL: {_request.request.url}, Response: {json_response}"
            self.log(response, "f")

        exit(1)

    def send_webhook(self, fail):
        color = 15158332

        if fail:
            webhook = DiscordWebhook(url=self.fail_webhook_url)

            # create embed object for webhook
            embed = DiscordEmbed(title="Application failure occurred", color=color)

            # set footer
            embed.set_footer(text='Rebel Notify')

            # set timestamp (default is now)
            embed.set_timestamp()

            # add embed object to webhook
            webhook.add_embed(embed)

            webhook.execute()
            return True

        for webhook_url in self.webhook_urls:
            webhook = DiscordWebhook(url=webhook_url)

            # create embed object for webhook
            embed = DiscordEmbed(title=f"{self.item_data['name']}",
                                 url="https://www.nike.cl" + self.item_data["detailUrl"],
                                 color=color)

            embed.set_thumbnail(url=self.item_data["imageUrl"])

            # set footer
            embed.set_footer(text='Rebel notify')

            # set timestamp (default is now)
            embed.set_timestamp()

            # add fields to embed
            # embed.add_embed_field(name='PID', color=color, value=self.pid)
            embed.add_embed_field(name='Precio',
                                  value=str(self.item_data["price"]))
            itemSize = self.item_data["name"].split(": ")[1].split(" -")[0]
            atcLink = f"https://www.nike.cl/checkout/cart/add?qty=1&redirect=true&sc=1&seller=1&sku={self.sku}"
            embed.add_embed_field(name=f'{self.sku}:',
                                  value=f"Talla: {itemSize} | [ATC]({atcLink})")

            # add embed object to webhook
            webhook.add_embed(embed)

            webhook.execute()

    def initialize(self):
        self.proxy_config()
        self.s = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "mobile": False,
                "platform": "windows"
            },
            requestPostHook=self.injection,
            captcha="vanaheim"
        )
        self.s.headers = OrderedDict([
            ('cache-control', 'max-age=0'),
            ('sec-ch-ua', '"Chromium";v="105", " Not A;Brand";v="99", "Google Chrome";v="105"'),
            ('sec-ch-ua-mobile', '?0'),
            ('sec-ch-ua-platform', '"Windows"'),
            ('upgrade-insecure-requests', '1'),
            ('dnt', '1'),
            ('user-agent', self.user_agent),
            ('accept',
             'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
            ('sec-fetch-site', 'none'),
            ('sec-fetch-mode', 'navigate'),
            ('sec-fetch-user', '?1'),
            ('sec-fetch-dest', 'document'),
            ('accept-encoding', 'gzip, deflate, br'),
            ('accept-language', 'en-US,en;q=0.9'),
        ])
        helheim.wokou(self.s)
        self.s.mount('http://', adapter)
        self.s.mount('https://', adapter)
        self.s.proxies = self.proxy
        self.s.bifrost_clientHello = 'chrome'

    def valid_alert(self):
        self.log("Checking for valid alert...", "p")

        if self.sku not in self.get_notified_skus():
            self.add_notified_sku()
            return True

        # Already notified
        self.log("Already notified. Resuming in 30 seconds...", "p")
        time.sleep(30)
        self.remove_notified_sku()
        return False

    def get_product(self):

        print(self.sku)
        addCartDATA = {
            "URL": "https://www.nike.cl/checkout/cart/add",
            "PARAMS": {
                "sku": str(self.sku),
                "qty": "1",
                "seller": "1",
                "sc": "1"
            },
            "HEADERS": {
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "dnt": "1",
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": 'Mac',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": self.user_agent
            }
        }
        cartDATA = {
            "URL": "https://www.nike.cl/api/checkout/pub/orderForm?refreshOutdatedData=true",
            "DATA": {
                "expectedOrderFormSections": [
                    "items",
                    "totalizers",
                    "clientProfileData",
                    "shippingData",
                    "paymentData",
                    "sellers",
                    "messages",
                    "marketingData",
                    "clientPreferencesData",
                    "storePreferencesData",
                    "giftRegistryData",
                    "ratesAndBenefitsData",
                    "openTextField",
                    "commercialConditionData",
                    "customData"
                ]
            }
        }
        time.sleep(0.01)

        helheim.bifrost(self.s,
                        'C:\\Users\\Administrator\\Downloads\\lanzamiento\\bifrost-0.1.7-windows.x86_64.dll')  # Replace this dll path.

        # Cart the product
        while True:
            print("Carting...")

            try:
                addCartGET = self.s.get(addCartDATA["URL"], params=addCartDATA["PARAMS"],
                                        headers=addCartDATA["HEADERS"])
                self.s.headers["origin"] = "https://www.nike.cl",
                self.s.headers["referer"] = "https://www.nike.cl/checkout/"
                # Check cart data for availability
                print("Checking cart data...")
                cartDataGET = self.s.get(cartDATA["URL"], json=cartDATA["DATA"], headers={'user-agent': self.user_agent})

                break
            except helheim.exceptions.HelheimBifrost:
                self.log("Request got timed out. Retrying...", "f")
                self.rotate_proxy()
                self.initialize()
                continue
            except Exception as exc:
                self.log(f"Unexpected error ({exc}). Resetting session and retrying...", "f")
                raise exc
                # self.rotate_proxy()
                # self.initialize()
                # continue

        cart_data = json.loads(json.dumps(xmltodict.parse(cartDataGET.text)))

        if not cart_data["OrderFormResponse"]["items"]:
            return False
        item_data = cart_data["OrderFormResponse"]["items"]["OrderItemResponse"]

        if type(item_data) == list:
            item_data = item_data[0]

        return item_data

    def monitor(self):

        while True:
            try:
                # Request
                self.item_data = self.get_product()
                if not self.item_data:
                    self.log("No stock (unloaded).", "f")
                    time.sleep(self.delay)
                    continue
                elif self.item_data["availability"] != "available":
                    self.log("No stock (loaded).", "f")
                    time.sleep(self.delay)
                    continue

                self.log(f"Found product for {self.sku}!", "S")

                # Check to see if it has already been alerted
                if self.valid_alert():
                    self.send_webhook(False)

                # Monitor Delay
                time.sleep(self.delay)
            except Exception as exc:
                self.log(f"Unexpected error ({exc}). Retrying...", "f")
                raise exc
                # self.rotate_proxy()
                # self.initialize()
                # continue

    def NikeCI(self):
        self.initialize()
        self.monitor()


if __name__ == "__main__":
    log("Collecting file info...", "BOT STARTUP", "p")

    # Proxies
    with open("proxies.txt", "r") as f:
        proxies = [line.replace("\n", "") for line in f.readlines()]

    with open("skus.txt", "r") as f:
        skus = [line.replace("\n", "") for line in f.readlines()]

    with open("settings.json", "r") as f:
        settings_file = json.load(f)

    log("Setting up thread lock...", "BOT STARTUP", "p")
    _taskLock = threading.Lock()
    _sessionLock = threading.Lock()
    _proxyLock = threading.Lock()

    for taskNum in range(len(skus)):
        if len(skus) > len(proxies):
            log("Proxy count must be equal or above sku count.", "BOT STARTUP", "F")
            exit(1)

        taskInstance = Task(
            sku=skus[taskNum],
            task_number=taskNum,
            settings=settings_file,
            proxy=proxies[taskNum],
            taskLock=_taskLock,
            sessionLock=_sessionLock,
            proxyLock=_proxyLock
        )
        proxies.pop(taskNum)
        log(f'Starting task...', taskInstance.task_number + 1, "p")
        threading.Thread(target=taskInstance.NikeCI, args=()).start()
