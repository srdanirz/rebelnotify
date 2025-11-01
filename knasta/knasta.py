import requests
from bs4 import BeautifulSoup
import dotenv
import datetime
import json
import time
import urllib3
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
CONFIG = dotenv.dotenv_values()


INSTOCK = []


def scrape_main_site(headers,url):
    items = []
    s = requests.Session()
    html = s.get(url=url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    soup = soup.find('script',  {'id': '__NEXT_DATA__'}).decode_contents()
    json_data = json.loads(soup)
    products = json_data['props']['pageProps']['initialData']['products']
    print(len(products))
    for product in products:
        item = [product['title'],
                product['current_price'],
                product['url'],
                product['image'],
                product['percent'],
                url] 
        items.append(item)
    return items


def discord_webhook(product_item):
    data = {}
    data["username"] = CONFIG['USERNAME']
    data["avatar_url"] = CONFIG['AVATAR_URL']
    data["embeds"] = []
    embed = {}
    if product_item == 'initial':
        embed["title"] = "Cache Cleared."
        embed["timestamp"] = str(datetime.datetime.utcnow())
        data["embeds"].append(embed)

        result = requests.post(CONFIG['WEBHOOK'], data=json.dumps(data), headers={"Content-Type": "application/json"})        
    else:
        embed["title"] = f'{product_item[0].upper()} [{product_item[4]}%]'  # Item 
        print(f'PRODUCT FOUND: {product_item[0]}')    
        embed["description"] = f"**[PRICE]:** {int(product_item[1])/1000}"
        if product_item[2] == "":
            embed['url'] = f'{product_item[5]}'  # Item link
        else:
            embed['url'] = f'{product_item[2]}'
        embed['thumbnail'] = {'url': product_item[3]} #Item Image
        embed["author"] = {'name': 'New Discount - knasta.cl', 'url':f'{product_item[5]}', 'icon_url': ''}
        embed["color"] = int(CONFIG['COLOUR'])
        embed["footer"] = {'text': 'Rebel Notify','icon_url': ''}
        embed["timestamp"] = str(datetime.datetime.utcnow())
        data["embeds"].append(embed)

        result = requests.post(CONFIG['WEBHOOK'], data=json.dumps(data), headers={"Content-Type": "application/json"})


    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Request delivered successfully, code {}.".format(result.status_code))



def checker(item):
    for product in INSTOCK:
        if product == item:
            return True
    return False


def remove_duplicates(mylist):
    return [list(t) for t in set(tuple(element) for element in mylist)]


def comparitor(item, start):
    if not checker(item):
        INSTOCK.append(item)
        if start == 0:
            discord_webhook(item)


def monitor():
    print('STARTING MONITOR')
    discord_webhook('initial')
    start = 1


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'knasta.cl',
    }

    keywords = (CONFIG['KEYWORDS']).split('%')
    i = 0
    print('Initial Listing Load Complete, checking for changes in future cycles.')
    while True:
        i = i + 1
        print(f'[{datetime.datetime.utcnow()}] [LOG] - Cycle #{i} Complete')
        urls = ['https://knasta.cl/results?category=20106&knastaday=3']
        j = 0
        for url in urls:
            j = j + 1
            print(f'    [{datetime.datetime.utcnow()}] [EVENT] - Checking Link #{j}')
            try:
                items = remove_duplicates(scrape_main_site(headers,url))
                for item in items:
                    check = False
                    if keywords == '':
                        comparitor(item, start)
                    else:
                        for key in keywords:
                            if key.lower() in item[0].lower():
                                check = True
                                break
                        if check:
                            comparitor(item, start)
                time.sleep(float(CONFIG['DELAY']))
            except Exception as e:
                print(f"Exception found '{e}' - Rotating proxy and user-agent")
                headers = {'User-Agent': user_agent_rotator.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'Host': 'knasta.cl',
                }
        start = 0

if __name__ == '__main__':
    urllib3.disable_warnings()
    monitor()
