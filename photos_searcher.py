


from src.searchers.ddg_searcher import DDGSearcher
from src.searchers.google_images_searcher import GoogleImagesSearcher
from src.parsers.google_images_parser import GoogleImagesParser
from src.parsers.sites_parser import SitesParser
from src.parsers.json_parser import JsonParser
from src.parsers.scopus_data_parser import ScopusDataParser
from src.utils.translator import GoogleTranslator

import os
import time
from datetime import datetime
from random import uniform
import aiofiles
import asyncio

out_path = './out'

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def save_image(img_bytes, name, extension, path):
    create_folder_if_not_exist(path)
    with open(f'{path}/{name}.{extension}', 'wb') as f:
        f.write(img_bytes)

def save_info(info_text, name, path):
    create_folder_if_not_exist(path)
    with open(f'{path}/{name}.txt', 'w') as f:
        f.write(info_text)

async def save_info_async(info_text, name, path):
    create_folder_if_not_exist(path)
    async with aiofiles.open(f'{path}/{name}.txt', 'w') as f:
        await f.write(info_text)

def search_info_ddg(author_name, path, name_prefix='ddg', site=None):
    query = author_name if not site else f'{author_name} site:{site}'
    links = DDGSearcher.ddg_search(query, delay=0)
    if links:
        print(f'{len(links)} found')
        links = links[:5]
        for i in range(len(links)):
            get_info_from_link(links[i], f'{name_prefix}_{i}', path)

async def search_info_ddg_async(author_name, path, name_prefix='ddg', site=None):
    query = author_name if not site else f'{author_name} site:{site}'
    links = DDGSearcher.ddg_search(query, delay=0)
    tasks = []
    if links:
        print(f'{len(links)} found')
        links = links[:5]
        for i in range(len(links)):
            if links[i]:
                tasks.append(get_info_from_link_async(links[i], f'{name_prefix}_{i}', path))
        await asyncio.gather(*tasks)

def search_author_photo(author_name, site, name, path):
    images_result_html = GoogleImagesSearcher.get_html_page_driver(f'{author_name} site:{site}')
    if images_result_html:
        images = GoogleImagesParser.get_images(images_result_html)
        if images:
            image = images[0]
            if image.has_face:
                img_bytes = image.img_bytes
                img_ext = image.extension
                save_image(img_bytes, name, img_ext, path)
            return [ img.url for img in images ]

def get_info_from_link(link, file_name, path):
    info = SitesParser.get_page_text(link)
    if info:
        save_info(info, file_name, path)

async def get_info_from_link_async(link, file_name, path):
    info = await SitesParser.get_page_text_async(link)
    if info:
        await save_info_async(info, file_name, path)

async def get_info_from_google_async(links, path):
    links = links[:5]
    tasks = []
    print(f'{len(links)} found')
    for j in range(len(links)):
        tasks.append(get_info_from_link_async(links[j], j, path))
    print(tasks)
    await asyncio.gather(*tasks)

def search_info_item(author_info):
    ru = author_info['ru']
    author_name = author_info['name']
    links = author_info['links']

    author_path = f'{out_path}/{author_name}'

    if ru:
        author_name = GoogleTranslator.translate_one(author_name)
        author_path = f'{out_path}/{author_name}'
    else:
        # search_info_ddg(author_name, author_path)
        asyncio.run(search_info_ddg_async(author_name, author_path))

    print('Author:', author_name, ', ru:', ru, ', out path:', author_path)

    for i in range(len(links)):
        link = links[i] if not ru else ScopusDataParser.remove_en_signs_link(links[i])
        print(f'link #{i+1}', link)
        img_links = search_author_photo(author_name, link, i, author_path)
        if ru:
            print('getting info from google')
            ###
            if img_links:
                asyncio.run(get_info_from_google_async(img_links, author_path))
            ###
        else:
            print('getting info from duckduckgo')
            # search_info_ddg(author_name, author_path, name_prefix=i, site=link)
            asyncio.run(search_info_ddg_async(author_name, author_path, name_prefix=i, site=link))
        time.sleep(uniform(2.0, 5.0))
        
def search_from_list(list_to_search):
    for author_info in list_to_search:
        search_info_item(author_info)

if __name__ == '__main__':
    test_data = JsonParser.read_json('ru_au1.json')
    search_list = ScopusDataParser.get_list_to_search(test_data)
    search_from_list(search_list)
