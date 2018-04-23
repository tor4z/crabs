from bs4 import BeautifulSoup
import re, json
from .url import URL, URLError

class Parser:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text

    def find_one(self, *args, **kwargs):
        raise NotImplemented

    def find_all(self, *args, **kwargs):
        raise NotImplemented

class HTMLParser(Parser):
    def __init__(self, text, url, parser = "html.parser"):
        self._parser = parser
        self._is_html = None
        self._soup_ = None
        self._url = url
        Parser.__init__(self, text)

    @property
    def _soup(self):
        if self._soup_ is None:
            self._soup_ = BeautifulSoup(self.text, self._parser)
        return self._soup_

    def find_all(self, *args, **kwargs):
        return self._soup.find_all(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        return self._soup.find(*args, **kwargs)

    def find_all_links(self, *args, **kwargs):
        links = self.find_all("a")
        urls = []
        for link in links:
            try:
                url = URL.urljoin(self._url.raw, link.get("href"))
                urls.append(url)
            except URLError:
                pass
        return urls

    @property
    def is_html(self):
        if self._is_html is None:
            self._is_html = bool(self._soup.find())
        return self._is_html

class StrParser(Parser):
    def __init__(self, text, pattern):
        self._re_obj = re.compile(pattern)
        Parser.__init__(self, text)
    
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

class JSONParser(Parser):
    def __init__(self, text):
        self._data = None
        Parser.__init__(self, text)

    def find_all(self, *args, **kwargs):
        return self.data.get(arg[0])

    def find_one(self, *args, **kwargs):
        return self.find_all(*args, **kwargs)

    def data(self):
        if self._data is None:
            self._data = json.loads(self.text)
        return self._data

    @property
    def is_json(self):
        try:
            self.data
            return True
        except:
            return False