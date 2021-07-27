
from src.searchers.google_images_searcher import GoogleImagesSearcher
from src.parsers.google_images_parser import GoogleImagesParser
from src.parsers.sites_parser import SitesParser
from src.parsers.json_parser import JsonParser
from src.parsers.scopus_data_parser import ScopusDataParser
from src.utils.translator import GoogleTranslator
from src.utils.file_writer import FileWriter
from src.utils.mysql import MySqlDatabase

import time
from random import uniform
import asyncio

out_path = './out'

def search_author_photo(author_name, site, name, path):
    images_result_html = GoogleImagesSearcher.get_html_page_driver(f'{author_name} site:{site}')
    if not images_result_html:
        return
    images = GoogleImagesParser.get_images(images_result_html)
    if not images:
        return
    image = images[0]
    if image.has_face:
        img_bytes = image.img_bytes
        img_ext = image.extension
        FileWriter.save_image(img_bytes, name, img_ext, path)
        # добавление в БД #
    return [ img.url for img in images ]

def get_info_from_link(link, file_name, path):
    info = SitesParser.get_page_text(link)
    if info:
        # добавление в БД #
        FileWriter.save_info(info, file_name, path)

async def get_info_from_link_async(link, file_name, path):
    info = await SitesParser.get_page_text_async(link)
    if not info:
        return
    print(f'recieved info from link {link}')
    link_text = f'Page link: {link}'
    separator = f'\n\n{"-"*len(link_text)}\n\n'
    info = link_text + separator + info
    # добавление в бд #
    await FileWriter.save_info_async(info, file_name, path)

async def get_info_from_google_async(links, path):
    links = links[:5]
    tasks = []
    for j in range(len(links)):
        tasks.append(get_info_from_link_async(links[j], j, path))
    await asyncio.gather(*tasks)

def search_info_item(author_info):
    ru = author_info['ru']
    name = author_info['name'] 
    if ru:
        name = GoogleTranslator.translate_one(name)
    links = author_info['links']
    author_path = f'{out_path}/{name}'

    print(f'Author: {name}, Total links: {len(links)}, Out path: {author_path}')

    for i in range(len(links)):
        link = links[i]
        if ru:
            link = ScopusDataParser.remove_en_signs_link(link)
        print(f'searching with link {link}')
        img_links = search_author_photo(name, link, i, author_path)
        if img_links:
            asyncio.run(get_info_from_google_async(img_links, author_path))
        time.sleep(uniform(2.0, 5.0))

        
def search_from_list(list_to_search):
    for author_info in list_to_search:
        search_info_item(author_info)

if __name__ == '__main__':
    test_data = JsonParser.read_json('authors_info_3l.json')
    search_list = ScopusDataParser.get_list_to_search(test_data)
    JsonParser.save_to_json(search_list, 'links.json')
    search_from_list(search_list)
