
from urllib.parse import urlencode
import requests
import selenium
from src.utils.req_headers import google_headers
# from src.utils.webdriver.webdriver import driver
from src.utils.remote_webdriver import driver
from selenium.common.exceptions import TimeoutException, WebDriverException

class GoogleImagesSearcher:

    @classmethod    
    def create_google_images_link(cls, text_to_search):
        params = dict(q=text_to_search, tbm='isch')
        link = f'https://www.google.com/search?{urlencode(params)}'
        return link

    @classmethod
    def get_html_page(cls, text_to_search):
        link = cls.create_google_images_link(text_to_search)
        response = requests.get(link, headers=google_headers)
        return response.text

    @classmethod
    def get_html_page_driver(cls, text_to_search):
        link = cls.create_google_images_link(text_to_search)
        try:
            driver.get(link)
        except (TimeoutException, WebDriverException) as e:
            print(e)
            return
        return driver.page_source
