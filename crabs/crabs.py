from crabs.data import Set

class Crabs:
    _ROUTE = None
    _SEEDS = []
    _URL_SET = Set()

    @classmethod
    def set_route(cls, route):
        cls._ROUTE = route

    @classmethod
    def set_seeds(cls, seeds):
        if not isinstance(seeds, list):
            raise TypeError("List required.")
        cls._SEEDS = seeds

    @classmethod
    def put_links(cls, links):
        if not isinstance(links, list):
            links = [links]
        for link in links:
            url = cls._ROUTE.dispatch_url(link)
            cls._URL_SET.add(url)

    @classmethod
    def run(cls):
        pass
