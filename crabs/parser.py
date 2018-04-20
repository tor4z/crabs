from bs4 import BeautifulSoup
import re
from crabs.url import URL

class HTMLParser:
    def __init__(self, page, parser = "html.parser"):
        self._parser = parser
        self._page = page
        self._soup_ = None
    
    @property
    def text(self):
        return self._page.text

    @property
    def _soup(self):
        if self._soup_ is None:
            self._soup_ = BeautifulSoup(self.text, self._parser)
        return self._soup_

    def find_all(self, *args, **kwargs):
        return self._soup.find_all(*args, **kwargs)

    def find_all_links(self, *args, **kwargs):
        links = self.find_all("a")
        urls = []
        for link in links:
            try:
                url = URL(link.get("href"), self._page.url)
                urls.append(url)
            except TypeError:
                pass
        return urls

class StrParser:
    def __init__(self, pattern):
        self._re_obj = re.compile(pattern)
    
    def _to_string(self, string):
        if isinstance(string, str) or isinstance(string, bytes):
            return string
        else:
            return str(string)

    def find_all(self, string):
        string = self._to_string(string)
        ret = [item for item in self._re_obj.findall(string) if item]
        return ret

    def find_one(self, string):
        string = self._to_string(string)
        m = self._re_obj.match(string)
        if m:
            return m.group(1)
        return None