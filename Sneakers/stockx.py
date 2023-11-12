import requests
from bs4 import BeautifulSoup
import pdb
import json
import cloudscraper

# got too lazy to get around the bot, copy and pasted myself lol

def get_data(sneaker):
    url = f"https://stockx.com/api/browse?_search={sneaker}"
    # headers = headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    session = cloudscraper.create_scraper()
    response = session.get(url)
    # response = requests.get(url=url, headers=headers)
    # data = response.json()
    pdb.set_trace()

if __name__ == "__main__":
    sneaker = 'kobe'
    get_data(sneaker)


