
from src.searchers.ddg_searcher import DDGSearcher
from src.parsers.json_parser import JsonParser

class SitesSearcher:

    found_sites_fname = 'found_sites.json'
    found_sites = dict()
    def __init__(self):
        if JsonParser.check_json_existing(self.found_sites_fname):
            self.found_sites = JsonParser.read_json(self.found_sites_fname)

    def search_university_site(self, university_name):
        if university_name in self.found_sites:
            print(f'site for {university_name} from cache')
            return self.found_sites[university_name]
        else:
            search_results = DDGSearcher.search_driver(university_name)
            if search_results:
                found_site = search_results[0]
                self.found_sites[university_name] = found_site
                JsonParser.save_to_json(self.found_sites, self.found_sites_fname)
                print(f'site for {university_name}: found, will be written to cache')
                return found_site



