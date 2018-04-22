import re, json
from .url import URL
from .client import Client, NotSuportMethodExp
from .parser import HTMLParser, JSONParser, StrParser
from .options import Method, TextType

class Handler:
    def __init__(self, url, method, headers={}):
        if not isinstance(url, URL):
            raise TypeError
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._url = url
        self._page = None
        self._method = method
        self._parsed = None
        self._client_ = None
        self._headers = headers
        self._text_type = None
        self._data = None
        self._status = None
        self._has_put_links = False
        self.init()

    def set_header(self, key, value):
        self._headers[key] = value

    def set_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._headers.update(headers)

    @property
    def _client(self):
        if self._client_ is None:
            self._client_ = Client(self.url, self.data, self.method)
            self._client_.set_headers(self._headers)
        return self._client_

    def set_data(self, data):
        if not isinstance(data, dict):
            raise TypeError("Dict required.")
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def method(self):
        return self._method

    @property
    def text_type(self):
        if self._text_type is None:
            text = self.page.text
            if self._json_parser().is_json:
                self._text_type = TextType.JSON
            if self._html_parser().is_html:
                self._text_type = TextType.HTML
            else:
                self._text_type = TextType.STRING
        return self._text_type
    
    def _html_parser(self):
        parser = HTMLParser(self.page)
        if parser.is_html:
            self._parsed = parser
        return parser

    def _json_parser(self):
        parser = JSONParser(self.page)
        if parser.is_json:
            self._parsed = parser
        return parser

    @property
    def status(self):
        if self._status is None:
            self._status = self._client.status
        return self._status

    @property
    def page(self):
        if self._page is None:
            if self.method == Method.GET:
                self._page = self._client.get()
            elif self.method == Method.POST:
                self._page = self._client.post()
            else:
                raise NotSuportMethodExp

            self._page = self._client.page
        return self._page

    @property
    def parsed(self):
        if self._parsed is None:
            if self.text_type == TextType.HTML:
                self._parsed = HTMLParser(self.page)
            elif self.text_type == TextType.JSON:
                self._parsed = JSONParser(self.page)
            else:  # string
                raise NotSupportStrParser
        return self._parsed

    @property
    def url(self):
        return self._url

    def links(self):
        if not self._has_put_links:
            if self.text_type == TextType.HTML:
                urls = self.parsed.find_all_links()
                self._has_put_links = True
                return urls
        return []

    def _check_status(self):
        if self.status != 200:
            raise HttpError(self.status)
    
    def execute(self):
        self._check_status()
        if self.method == Method.GET:
            self.get()
        elif self.method == Method.POST:
            self.post()
        else:
            raise NotSuportMethodExp

    def init(self):
        pass

    def get(self):
        pass

    def post(self):
        pass

class DefaultHandler(Handler):
    pass

class HttpError(Exception):
    pass

class NotSupportStrParser(Exception):
    pass