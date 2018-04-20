import re, json
from crabs.url import URL
from crabs.client import Client
from crabs.parser import HTMLParser, JSONParser, StrParser
from crabs.options import method, text_type

class Handler:
    def __init__(self, url, method):
        if not isinstance(url, URL):
            raise TypeError
        self._url = url
        self._page = None
        self._method = method
        self._parsed = None
        self._client_ = None
        self._headers = {}
        self._text_type = None
        self._data = None
        self._status = None
        self.init()

    def set_header(self, key, value):
        self._headers[key] = value

    def _client(self):
        if self._client_ is None:
            self._client_ = Client()
            self._client_.set_headers(self._headers)
        return self._client_

    def set_data(self, data):
        if not isinstance(data, dict):
            raise TypeError("Dict required.")
        self._data = data

    @property
    def text_type(self):
        if self._text_type is None:
            text = self.page.text
            if self._json_parser().is_json:
                self._text_type = text_type.JSON
            if self._html_parser().is_html:
                self._text_type = text_type.HTML
            else:
                self._text_type = text_type.STRING
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
            if self._method == method.GET:
                self._page = self._client.get(self.url)
            elif self._method == method.POST:
                self._page = self._client.post(self.url, data = self._data)
            else:
                raise NotSuportMethodExp

            self._page = client.page
        return self._page

    @property
    def parsed(self):
        if self._parsed is None:
            if self._text_type == text_type.HTML:
                self._parsed = HTMLParser(self.page)
            elif self._text_type == text_type.JSON:
                self._parsed = JSONParser(self.page)
            else:  # string
                self._parsed = StrParser(self.page)
        return self._parsed

    @property
    def url(self):
        return self._url

    def _put_links(self):
        pass

    def init(self):
        pass

    def get(self):
        pass

    def post(self):
        pass

class NotSuportMethodExp(Exception):
    pass