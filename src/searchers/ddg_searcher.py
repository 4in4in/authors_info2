
import time

from urllib.parse import urlencode
import requests

from bs4 import BeautifulSoup
from requests.sessions import session

from src.utils.req_headers import simple_headers

class DDGSearcher:

    @classmethod
    def create_ddg_link(cls, text_to_search):
        params = dict(q=text_to_search)
        link = f'https://duckduckgo.com/html/?{urlencode(params)}'
        # link = f'https://html.duckduckgo.com/html/?{urlencode(params)}'
        return link

    @classmethod
    def ddg_search(cls, text_to_search, delay=0.05):
        ddg_link = cls.create_ddg_link(text_to_search)
        if delay:
            time.sleep(delay)
        try:
            response = requests.get(ddg_link, headers=simple_headers, timeout=3)
        except Exception as e:
            print(e)
        else:
            print(ddg_link, response.status_code)
            if response.status_code == 200:
                html_doc = response.text
                soup = BeautifulSoup(html_doc, features='html.parser')
                result_a_tags = soup.findAll('a', class_='result__a', href=True)
                result_links = [ link['href'] for link in result_a_tags if 'duckduckgo.com' not in link['href'] ]
                return result_links