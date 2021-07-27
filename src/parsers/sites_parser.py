
from bs4 import BeautifulSoup

import aiohttp
import re
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectorSSLError, ClientConnectorError
from src.utils.req_headers import simple_headers

class SitesParser:
    @classmethod
    def get_page_text(cls, link):
        try:
            response = requests.get(link, headers=simple_headers, timeout=(5, 5))
        except (HTTPError, ConnectionError, Timeout, RequestException, OSError) as e:
            print(e)
        else:
            if response.status_code == 200:
                print(response.headers.get('Content-Type'))
                if 'text/html' in response.headers.get('Content-Type'):
                    html_doc = BeautifulSoup(response.text, features='html.parser')

                    if main_tag := html_doc.find('html'):
                        normalized_text = re.sub(r'\n\s*\n', '\n\n', main_tag.getText())
                        content = f'Page link: {link}\n\n{normalized_text}'
                        return content

    @classmethod
    async def get_page_text_async(cls, link):
        params = dict(
            headers=simple_headers,
            timeout=5,
            verify_ssl=False
        )
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link, **params) as response:
                    if 'Content-Type' not in response.headers: 
                        return
                    if 'text/html' not in response.headers['Content-Type']: 
                        return
                    html_text = await response.text(errors='ignore')
                    html_doc = BeautifulSoup(html_text, features='html.parser')
                    if html_doc.find('html'):
                        info = cls.normalize_page_text(html_doc.find('html').getText(' '))
                        return info
            except (TimeoutError, ClientConnectorSSLError, ClientConnectorError) as e:
                print(e)

    @classmethod
    def normalize_page_text(cls, text):
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n ', '\n', text)
        return text

if __name__ == '__main__':
    x = SitesParser.get_page_text('https://www.uib.no/en/persons/Srisuda.Chaikitkaew')
    print(x)