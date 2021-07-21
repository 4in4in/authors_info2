
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
            return self.found_sites[university_name]
        else:
            search_results = DDGSearcher.ddg_search(university_name, delay=0.05)
            if search_results:
                found_site = search_results[0]
                self.found_sites[university_name] = found_site
                JsonParser.save_to_json(self.found_sites, self.found_sites_fname)
                return found_site



