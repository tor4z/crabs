from urllib.parse import urlsplit, urljoin

class Page:
    def __init__(self, text, url):
        self._url = url
        self._text = text
        self._domain = None
        self._scheme = None
        self._url_split_ = None
        self._netloc = None

    @property
    def _url_split(self):
        if self._url_split_ is None:
            self._url_split_ = urlsplit(self.url)
        return self._url_split_

    @property
    def text(self):
        return self._text

    @property
    def url(self):
        return self._url

    @property
    def netloc(self):
        if self._netloc is None:
            self._netloc = self._url_split.netloc
        return self._netloc

    @property
    def scheme(self):
        if self._scheme is None:
            self._scheme = self._url_split.scheme
        return self._scheme