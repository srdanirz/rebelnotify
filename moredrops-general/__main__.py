import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import traceback
import threading
import time

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType
from fp.fp import FreeProxy
from db import engine, Products
from sqlalchemy.orm import Session

from config import Discord, Configuration

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)

proxy_object = FreeProxy(country_id=['GB', 'US', 'CL'], rand=True)
session = Session(engine)

def scrape_site(headers, proxy, session):
    page = 1
    s = requests.Session()
    while page < 2:
        url = f'https://moredrops.cl/Drops/Men/Footwear/Sneakers-Men/c/dropsHombreFootwearSneakers?q=%3Acreationtime&page={page}'
        html = s.get(url=url, headers=headers, proxies=proxy)
        soup = BeautifulSoup(html.text, 'html.parser')
        products = soup.find_all('div', {'class': 'product-item'})
        
        for product in products:
            try:
                name = product.find('a', {'class':'name'}).text
                price = product.find('div', {'class':'item--price'}).text
                img = product.find('img')['src']
                product_url = product.find('a', {'class': 'name'})['href']
                sku = product_url.split('/')[-1]

                query = session.query(Products).filter_by(title=name, sku=sku).first()

                if query is None:
                    discord_webhook(
                        title=name,
                        url=product_url,
                        thumbnail=img,
                        sku=sku,
                        price=price
                    )
                    session.add(Products(title=name, sku=sku))
                    session.commit()
            
            except:
                print(traceback.format_exc())
                pass


def discord_webhook(title, url, thumbnail, sku, price):
    data = {
        "username": Discord.USERNAME,
        "avatar_url": Discord.AVATAR_URL,
        "embeds": [{
            "title": title,
            "url": url,
            "thumbnail": {"url": thumbnail},
            "color": int(Discord.COLOUR),
            "footer": {
                "text": Discord.FOOTER_TEXT,
                "icon_url": Discord.FOOTER_URL
                },
            "timestamp": str(datetime.utcnow()),
            "fields": [
                {"name": "SKU", "value": sku},
                {"name": "Price", "value": price},
                {"name": "Stock", "value": "In Stock"}
            ]
        }]
    }

    result = requests.post(Discord.WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


def monitor():
    print('STARTING MONITOR')
    if Configuration.ENABLE_FREE_PROXY:
        proxy = {'http': proxy_object.get()}
    else:
        proxy = {}

    if Configuration.USERAGENT == '':
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': user_agent_rotator.get_random_user_agent(),
        }
    else:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': Configuration.USERAGENT
        }

    while True:
        try:
            scrape_site(headers, proxy, session)
        
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ContentDecodingError,
            requests.exceptions.HTTPError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.SSLError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
            requests.exceptions.TooManyRedirects,
            Exception
        ) as e:
            print(traceback.format_exc())
            if Configuration.USERAGENT == '':
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'User-Agent': user_agent_rotator.get_random_user_agent(),
                    'Cookie': 'anonymous-consents=%5B%5D; _fbp=fb.1.1638632779418.2127183456; __utmc=140877358; cookie-notification=ACCEPTED; ROUTE=.accstorefront-54bc79dd8c-ltcc4; __utma=140877358.1302538391.1638632779.1639178290.1639231061.3; __utmz=140877358.1639231061.3.2.utmcsr=yaneken.queue-it.net|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=140877358.1.10.1639231061; JSESSIONID=Y0-20c14647-aaf5-4ba7-9490-8764fde8013e.accstorefront-54bc79dd8c-ltcc4; QueueITAccepted-SDFrts345E-V3_drops89=EventId%3Ddrops89%26QueueId%3Dbc1cb8bb-6967-46cc-b5f5-a124dc70175e%26RedirectType%3Dsafetynet%26IssueTime%3D1639233630%26Hash%3Dde4652d4530bca85b13a9dc444f2d694b585a14bde941a0edd4a3b4b4ac9622d'
                }

            if Configuration.ENABLE_FREE_PROXY:
                proxy = {'http': proxy_object.get()}
            else:
                proxy = {}


        time.sleep(2.5)


if __name__ == '__main__':
    threads = []
    for i in range(2):
        x = threading.Thread(target=monitor)
        threads.append(x)
        x.start()
        time.sleep(0.5)
    
