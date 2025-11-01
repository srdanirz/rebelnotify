import requests
import logging
import dotenv
import datetime
import json
import time
import urllib3
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

logging.basicConfig(filename='test.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s',
                    level=logging.DEBUG)

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
CONFIG = dotenv.dotenv_values()


INSTOCK = []


def scrape_main_site(headers,url):
    items = []
    s = requests.Session()
    html = s.get(url=url, headers=headers, verify=False, timeout=15)
    json_data = json.loads(html.text)
    for product in json_data:
        item = [product["productName"],
                product["link"],
                product["productReference"],
                product["releaseDate"],
                product["releaseHour"][0],
                product["items"][0]["images"][0]["imageUrl"],
                product["items"][0]["color"][0]]
        sizes = []
        for size in product["items"]:
            if size["sellers"][0]["commertialOffer"]["IsAvailable"] != False:
                sizes.append(f'[**US {size["talle"][0]}**] - [QTY: {size["sellers"][0]["commertialOffer"]["AvailableQuantity"]}]')
            else:
                sizes.append(f'[**US {size["talle"][0]}**]({size["sellers"][0]["addToCartLink"]})')
                #sizes.append(f'**US {size["talle"][0]}**')
        sizesStr =  '\n'.join(sizes)
        item.append(sizesStr)    
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
        embed["title"] = product_item[0].upper()  # Item 
        embed['url'] = f'{product_item[1]}'  # Item link
        embed['thumbnail'] = {'url': product_item[5]} #Item Image
        embed["description"] = f'**Sizes**: \n\n {product_item[7]}'  # Item color
        embed["author"] = {'name': 'Product Added @ SNKRS Chile', 'url':'https://www.nike.cl/snkrs/futuros', 'icon_url': 'https://thumbs.dreamstime.com/b/web-183282388.jpg'}
        embed["fields"] = [{'name': 'SKU', 'value': f'{product_item[2]}', 'inline': True},
            {'name': 'Color', 'value': f'{product_item[6]}', 'inline': True},
            {'name': '\u200b', 'value': '\u200b', 'inline': True},
            {'name': 'Release Date', 'value': f'{product_item[3].split("T")[0]}', 'inline': True},
            {'name': 'Release Hour', 'value': f'{product_item[4]}', 'inline': True}]
        embed["color"] = int(CONFIG['COLOUR'])
        embed["footer"] = {'text': 'Rebel Notify','icon_url': 'https://i.imgur.com/x9Vsn7m.jpg'}
        embed["timestamp"] = str(datetime.datetime.utcnow())
        data["embeds"].append(embed)

        result = requests.post(CONFIG['WEBHOOK'], data=json.dumps(data), headers={"Content-Type": "application/json"})


    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        logging.error(msg=err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

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
    logging.info(msg='Successfully started monitor')
    discord_webhook('initial')
    start = 1

    headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
    keywords = CONFIG['KEYWORDS'].split('%')
    negative_keywords = CONFIG['NEG_KEYWORDS'].split('%')
    i = 0
    print('Initial Listing Load Complete, checking for changes in future cycles.')
    while True:
        i = i + 1
        print(f'[{datetime.datetime.utcnow()}] [LOG] - Cycle #{i} Complete')
        urls = ['https://www-nike-cl.translate.goog/api/catalog_system/pub/products/search?fq=B:2000002&_from=0&_to=49&O=OrderByReleaseDateDESC&_x_tr_sl=el&_x_tr_tl=en&_x_tr_hl=en-GB&_x_tr_pto=wapp']
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
                        for neg_key in negative_keywords:
                            if neg_key.lower() in item[0].lower():
                                check = False
                                break
                        if check:
                            comparitor(item, start)
                time.sleep(float(CONFIG['DELAY']))
                
            except Exception as e:
                print(f"Exception found '{e}' - Rotating proxy and user-agent")
                logging.error(e)
                headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
        start = 0

if __name__ == '__main__':
    urllib3.disable_warnings()
    monitor()
