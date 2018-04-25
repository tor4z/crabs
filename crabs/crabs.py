from .route import Route
from .options import Travel, Method
from .logs import Log
from .handler import DefaultHandler
from .url_pool import URLPool, URLPoolEmpty
from .threadpool.threadpool import ThreadPoolExecutor, ExecutorSetTwice
from .http_client.url import URL, URLError
from .http_client.utils import ClientHeaders
from .http_client.client import (Client, 
                                HttpError, 
                                ClientTooManyRedirects, 
                                HttpConnError)

class Crabs:
    def __init__(self):
        self._routes = Route()
        self._url_pool = URLPool()
        self.logger = Log(self.__class__.__name__)
        self.client = Client()
        self._enable_threadpool = False
        self._initialized = False
        self._scraped_count = 0

    @property
    def report(self):
        return "scraped({0})".format(self._scraped_count)

    def set_http_client(self, headers=None, max_redirects=None, html_parser=None):
        self.client.update_headers(headers)
        self.client.set_max_redirects(max_redirects)
        self.client.set_html_parser(html_parser)

    def set_logger(self, name=None, format=None, level=None, file=None):
        self.logger.set_name(name)
        self.logger.set_format(format)
        self.logger.set_level(level)
        self.logger.set_file(file)

    def set_url_filter(self, allow_netlocs=None, disallow_paths=None):
        self._url_pool.set_allow_netloc(allow_netlocs)
        self._url_pool.set_disallow_path(disallow_paths)

    def set_scraper(self, depth=None, travel_mod=None):
        self._url_pool.set_max_depth(depth)
        self._url_pool.set_treval_mod(travel_mod)

    def set_routes(self, routes):
        self._routes.update_routes(routes)

    def set_seeds(self, urls):
        if not isinstance(urls, list):
            raise TypeError("List required.")
        self._url_pool.put_urls(urls)

    def set_executor(self, max_size=None, queue_cls=None, task_size=None):
        if self._enable_threadpool:
            raise ExecutorSetTwice("Executor can not set twice.")
        self._enable_threadpool = True
        self._threadpool_max_size = max_size
        self._threadpool_queue_cls = queue_cls
        self._threadpool_task_size = task_size
        self._threadpool_executor = ThreadPoolExecutor(
                                    self._threadpool_max_size, 
                                    self._threadpool_queue_cls,
                                    self._threadpool_task_size,
                                    self.logger)

    @property
    def executor(self):
        if self._enable_threadpool:
            return self._threadpool_executor
        else:
            raise RuntimeError("Threadpool disabled.")

    def initialize(self):
        if not self._initialized:
            self._initialized = True

    def _put_urls_from_resp(self, resp):
        try:
            for url in resp.html.find_all_links():
                url = self._url_pool.new_url(url, depth = resp.depth + 1)
                self._url_pool.put_url(url)
        except TypeError:
            pass

    def _exec_handler(self, handler):
        try:
            resp = handler.execute()
            self._put_urls_from_resp(resp)
            self._scraped_count += 1
        except HttpError as e:
            self.logger.warning("HttpError({0}):{1}".format(e, handler.url))
        except ClientTooManyRedirects as e:
            self.logger.warning(e)
        except HttpConnError as e:
            self.logger.warning(e)

    def report_collections(self):
        reports = self.report + "|" +\
                  self.logger.report + "|" +\
                  self.client.report + "|" +\
                  self._url_pool.report + "|" +\
                  self.executor.report if self._enable_threadpool else ""
        print(reports, end="\r")

    def _exec_route(self, url):
        self.logger.info("Scraping({0}): {1}".format(url.depth, url))
        self.report_collections()
        handler_cls, url, method = self._routes.dispatch(url)
        if handler_cls is None:
            handler_cls = DefaultHandler
            method = Method.GET
        handler = handler_cls(url, method, self)
        self._exec_handler(handler)

    def _route_loop(self):
        while True:
            url = self._url_pool.get_url(block=True)
            if self._enable_threadpool:
                self.executor.submit(self._exec_route, url)
            else:
                self._exec_route(url)

    def run(self):
        try:
            self.initialize()
            self._route_loop()
        except KeyboardInterrupt:
            self.logger.info("Exit.")
        except URLPoolEmpty:
            self.logger.fatal("URL set empty.")

        self.shutdown()

    def shutdown(self, wait=True):
        if self._enable_threadpool:
            self.executor.shutdown(wait)