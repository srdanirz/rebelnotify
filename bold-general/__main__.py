import requests
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
    while page < 5:
        url = f'https://api.cxl8rgz-articulos1-p1-public.model-t.cc.commerce.ondemand.com/rest/v2/boldb2cstore/products/search?fields=products(url%2Ccode%2Cbadges%2Cname%2Csummary%2Cprice(FULL)%2CregularPrice(formattedValue)%2Cimages(DEFAULT)%2Cstock(FULL)%2CaverageRating%2CvariantOptions%2Ccategories(DEFAULT)%2CformattedDiscount)%2Cfacets%2Cbreadcrumbs%2Cpagination(DEFAULT)%2Csorts(DEFAULT)%2CfreeTextSearch%2CcurrentQuery%2CspellingSuggestion&query=%3ADEFAULT%3AallCategories%3AboldMarcas&currentPage={page}&pageSize=50&lang=es_CL&curr=CLP'
        html = requests.get(url=url, headers=headers, proxies=proxy)
        data = json.loads(html.text)

        for product in data['products']:
            query = session.query(Products).filter_by(title=product['name'], code=product['code']).first()

            if product['stock']['stockLevelStatus'] == 'inStock' and query is None:
                
                discord_webhook(
                    title=product['name'],
                    url=product['url'],
                    thumbnail=product['images'][0]['url'],
                    sku=product['code'],
                    stock_level=product['stock']['stockLevel'],
                    price=product['price']['formattedValue']
                )
                
                #print(product['name'])
                session.add(Products(title=product['name'], code=product['code']))
                session.commit()
                


            elif product['stock']['stockLevelStatus'] != 'InStock' and query is not None:
                session.delete(query)
                session.commit()


def discord_webhook(title, url, thumbnail, sku, stock_level, price):
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
                {"name": "Stock Level", "value": str(stock_level)},
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
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': user_agent_rotator.get_random_user_agent()
        }
    else:
        headers = {
            'Accept': 'application/json, text/plain, */*',
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
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'User-Agent': user_agent_rotator.get_random_user_agent()
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
    
