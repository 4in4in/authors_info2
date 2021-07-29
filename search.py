

from src.parsers.google_images_parser import GoogleImagesParser
from src.parsers.scopus_data_parser import ScopusDataParser
from src.parsers.sites_parser import SitesParser
from src.searchers.sites_searcher import SitesSearcher
from src.searchers.google_images_searcher import GoogleImagesSearcher
from connector import Database, ScopusAuthor
from src.utils.file_writer import FileWriter
from src.utils.translator import GoogleTranslator
from random import uniform
from time import sleep


class Searcher:
    sites_searcher = SitesSearcher()

    out_path = './out'

    def search(self, authors_list):
        if not authors_list:
            return 'No authors to search.'
        prepared_list = self.prepare_authors_list(authors_list)
        ### удалять повторяющиеся адреса
        for author_info in prepared_list:
            self.search_author(author_info)

    def prepare_authors_list(self, authors_list, search_site=False):
        result = []
        for author_info in authors_list:
            if author_info.url is None and not search_site:
                continue
            if (author_info.url is None and author_info.affiliation_name is not None):
                author_info.url = self.sites_searcher.search_university_site(author_info.affiliation_name)
            if author_info.country == 'Russian Federation':
                author_info.url = ScopusDataParser.remove_en_signs_link(author_info.url)
            result.append(author_info)
        return result

    def get_name_to_search(self, author_info: ScopusAuthor):
        if author_info.first_name and author_info.last_name:
            name = author_info.first_name +' '+author_info.last_name
        else:
            name = author_info.indexed_name
        if author_info.country == 'Russian Federation':
            name = GoogleTranslator.translate_one(name)
        return name


    def search_author(self, author_info: ScopusAuthor, total_results=1):
        name = self.get_name_to_search(author_info)
        url = author_info.url
        query = f'{name} site:{url}'
        print(f'name: {name}, url: {url}')
        gimg_html = GoogleImagesSearcher.get_html_page_driver(query)
        images = GoogleImagesParser.get_images(gimg_html)
        if not images:
            return
        total_results = len(images) if len(images) < total_results else total_results
        for i in range(total_results):
            info_raw = SitesParser.get_page_text(images[i].url)
            if info_raw:
                print(f'saving info from {images[i].url}')
                Database.write_raw_info(author_info.author_id, images[i].url, info_raw)
            
            if images[i].has_face:
                file_name = f'{author_info.author_id}_{author_info.affiliation_id}_{i}'
                saved_path = self.save_image(images[i], file_name)
                print(f'saving photo: {saved_path}')
                Database.write_img_info(author_info.author_id, saved_path)
        sleep(uniform(2.0, 5.0))

    def save_image(self, image, name):
        saved_path = FileWriter.save_image(image.img_bytes, name, image.extension, self.out_path)
        return saved_path


if __name__ == '__main__':
    searcher = Searcher()
    authors_to_search = Database.get_authors()
    searcher.search(authors_to_search)