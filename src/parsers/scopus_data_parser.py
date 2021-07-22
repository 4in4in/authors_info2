import re
from src.parsers.json_parser import JsonParser
from src.searchers.sites_searcher import SitesSearcher

sites_searcher = SitesSearcher()

class ScopusDataParser:

    @classmethod
    def get_universities_authors_list(cls, author_retrieval_response):
        items_to_search = []

        for response_data in author_retrieval_response:
            author_info = cls.get_author_universities(response_data)
            if author_info:
                items_to_search.append(cls.get_author_universities(response_data))

        return items_to_search

    @classmethod
    def get_author_universities(cls, response_data):
        scopus_id = response_data['coredata']['dc:identifier']
        author_profile = response_data['author-profile']

        name = cls.get_author_name(author_profile)
        affiliation_current = cls.get_affiliation(author_profile, 'affiliation-current')
        affiliation_history = cls.get_affiliation(author_profile, 'affiliation-history')

        if name:
            return dict(
                scopus_id=scopus_id,
                name=name,
                affiliation_current=affiliation_current,
                affiliation_history=affiliation_history
            )
        else:
            return None
    
    @classmethod
    def get_author_name(cls, author_profile):
        preferred_name = author_profile.get('preferred-name')
        if preferred_name:
            if ('surname' and 'given-name' in preferred_name):
                return ' '.join([
                    preferred_name['surname'],
                    preferred_name['given-name']
                    ])
            else:
                return preferred_name['indexed-name']
        else:
            return None

    @classmethod
    def get_affiliation(cls, author_profile, affiliation_name):
        if afflilation_current := author_profile.get(affiliation_name):
            if afflilation := afflilation_current.get('affiliation'):
                return cls.get_universities_from_affiliation(afflilation)

    @classmethod
    def get_universities_from_affiliation(cls, affiliation_data):
        universities_data = []
        if isinstance(affiliation_data, dict):
            if ip_doc := affiliation_data.get('ip-doc'):
                university_info = cls.get_university_info(ip_doc)
                universities_data.append(university_info)
        elif isinstance(affiliation_data, list):
            for affiliation in affiliation_data:
                if ip_doc := affiliation.get('ip-doc'):
                    university_info = cls.get_university_info(ip_doc)
                    universities_data.append(university_info)
        return universities_data

    @classmethod
    def get_university_info(cls, ip_doc):
        if 'afdispname' in ip_doc:
            name = ip_doc['afdispname']
            url = ip_doc.get('org-URL')
            address = ip_doc.get('address')
            country_code = address.get('@country') if address else None

            if url is None:
                url = sites_searcher.search_university_site(name)

            university_info = dict(
                name=name,
                url=url,
                country_code=country_code
            )
            return university_info

    @classmethod
    def get_list_to_search(cls, author_retrieval_response):
        prepared_data = author_retrieval_response
        names_and_urls_list = []
        for author_object in prepared_data:
            name = author_object['name']
            links = []
            ru = False
            for affil_type in ['affiliation_current', 'affiliation_history']:
                if affil := author_object.get(affil_type):
                    for university_object in affil:
                        if university_object is not None:
                            url = university_object.get('url')
                            if not ru and cls.check_ru_link(url):
                                ru = True
                            if url and url not in links:
                                links.append(url)
            names_and_urls_list.append({'name': name, 'links': links, 'ru': ru})
        return names_and_urls_list

    @classmethod
    def remove_en_signs_link(cls, link):
        en_signs = ['en','eng','english','us']

        en_signs.sort(key=len, reverse=True)

        for sign in en_signs:
            link = re.sub(r'^{}\.'.format(sign), '', link)
            link = re.sub(r'/{}\.'.format(sign), '/', link)
            link = re.sub(r'/{}/'.format(sign), '', link)
            link = re.sub(r'/{}$'.format(sign), '', link)
                
        return link

    @classmethod
    def check_ru_link(cls, link):
        ru_signs = [ 'ru', 'ua', 'by', 'kz', 'uz' ]
        for sign in ru_signs:
            if re.findall(r'\.{}'.format(sign), link):
                return True
            if re.findall(r'^{}\.'.format(sign), link):
                return True
            if re.findall(r'/{}\.'.format(sign), link):
                return True
        return False

if __name__ == '__main__':
    # list_without_links = JsonParser.read_json('authors_info.json')
    # list_with_links = ScopusDataParser.get_universities_authors_list(list_without_links[0]['author-retrieval-response-list']['author-retrieval-response'])
    # JsonParser.save_to_json(list_with_links, 'authors_info_0l.json')
    list_without_links = JsonParser.read_json('author_infos_raw.json')
    list_with_links = ScopusDataParser.get_universities_authors_list(list_without_links)
    JsonParser.save_to_json(list_with_links, 'ru_au4.json')
    ...