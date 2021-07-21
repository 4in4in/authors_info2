
import requests

from src.utils.req_headers import scopus_headers
from src.parsers.json_parser import JsonParser

class ScopusInfo:

    @classmethod
    def get_author_info(cls, scopus_id):
        response = requests.get(
            f'https://api.elsevier.com/content/author/author_id/{scopus_id}',
            headers=scopus_headers
            )
        return response.json()

    @classmethod
    def get_author_info_test(cls, author_ids):
        base_url = 'https://api.elsevier.com/content/author'
        url_query = f'{base_url}?view=ENHANCED&author_id={",".join(author_ids)}'
        response = requests.get(url_query, headers=scopus_headers)
        return response.json()

if __name__ == '__main__':
    id = 57223088165
    id2 = 57223194367
    author_info = ScopusInfo.get_author_info(id)
    JsonParser.save_to_json(author_info, f'{id}.json')

    authors_info_test = ScopusInfo.get_author_info_test([str(id), str(id2)])
    JsonParser.save_to_json(authors_info_test, f'ids_test.json')