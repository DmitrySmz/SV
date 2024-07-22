import requests
from bs4 import BeautifulSoup

URL = ''
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


def get_html_any(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content_any(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('span', class_='text-2xl')
    item = str(items[0])[57:].rstrip('</span>')
    return item


def parse_any(URL):
    html = get_html_any(URL)
    if html.status_code == 200:
        item = get_content_any(html.text)
        return item
    else:
        print('error')
