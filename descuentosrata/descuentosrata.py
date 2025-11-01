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
    products = soup.find_all('div',  {'class': 'my-2 col-md-4 col-lg-3 col-6'})
    print(len(products))
    for product in products:
        item = [product.find('span', {'class':'font-weight-bold'}).text.strip(),
                product.find('span', {'class':'font-weight-normal'}).text.strip(),
                product.find('a')['href'],
                product.find('div', {'class':'img-responsive'})['style'],
                url] 
        items.append(item)
    return items


def discord_webhook(product_item):
    """
    Sends a Discord webhook notification to the specified webhook URL
    :param product_item: An array of the product's details
    :return: None
    """

    
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
        product_image = product_item[3].split('url(')[1].split(')')[0]
        embed["title"] = f'{product_item[0].upper()}'  # Item 
        print(f'PRODUCT FOUND: {product_item[0]}')    
        embed["description"] = f"**[PRICE/DISC]:** {product_item[1]}"
        embed['url'] = f'https://descuentosrata.com{product_item[2]}'
        embed['thumbnail'] = {'url': product_image} #Item Image
        embed["author"] = {'name': 'New Discount - DESCUENTOSRATA', 'url':'', 'icon_url': ''}
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
    print('STARTING CYCLES - DESCUENTOSRATA')
    discord_webhook('initial')
    start = 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'descuentosrata.com',
    }

    keywords = (CONFIG['KEYWORDS']).split('%')
    i = 0
    print('Initial Listing Load Complete, checking for changes in future cycles.')
    while True:
        i = i + 1
        print(f'[{datetime.datetime.utcnow()}] [LOG] - Cycle #{i} Complete')
        urls = ['https://descuentosrata.com/']
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
                headers = {
                    'User-Agent': user_agent_rotator.get_random_user_agent(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-IN,en-GB;q=0.9,en;q=0.8',
                    'Connection': 'keep-alive',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    'Host': 'descuentosrata.com',
                }
        start = 0

if __name__ == '__main__':
    urllib3.disable_warnings()
    monitor()
