from queue import PriorityQueue
from crabs.url import URL, URLError
from crabs.route import Route

class Crabs:
    def __init__(self):
        self._routes = None
        self._seed = []
        self._urls = PriorityQueue()
        self._initialized = False

    def set_routes(self, routes):
        self._routes = Route()
        self._routes.set_routes(routes)

    def set_seeds(self, seeds):
        if not isinstance(seeds, list):
            raise TypeError("List required.")
        self._seed = seeds

    def _init_seed(self):
        for url in self._seed:
            if not URL.is_full_url(url):
                raise URLError
            self._urls.put(URL(url))

    def initialize(self):
        if not self._initialized:
            self._init_seed()
            self._initialized = True

    def put_links(self, urls):
        if urls:
            if not isinstance(urls, list):
                urls = [urls]
            if not isinstance(urls[0], URL):
                raise TypeError
        
            for url in urls:
                if isinstance(url, URL):
                    self._urls.put(url)
                elif isinstance(url, str):
                    self._urls.put(URL(url))
                else:
                    raise TypeError

    def _get_url(self, *args, **kwargs):
        return self._urls.get(*args, **kwargs)

    def _exec_handler(self, handler):
        handler.execute()
        urls = handler.links()
        self.put_links(urls)

    def _route_loop(self):
        while True:
            url = self._get_url(block=False)
            handler = self._routes.dispatch(url)
            self._exec_handler(handler)

    def run(self):
        self.initialize()
        self._route_loop()