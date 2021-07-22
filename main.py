

from src.parsers.scopus_data_parser import ScopusDataParser
from src.parsers.json_parser import JsonParser

list_without_links = JsonParser.read_json('author_infos_raw.json')
list_with_links = ScopusDataParser.get_universities_authors_list(list_without_links)
JsonParser.save_to_json(list_with_links, 'ru_au4.json')

