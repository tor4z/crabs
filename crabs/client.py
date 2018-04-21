from requests import Request, Session
from crabs.page import Page
from crabs.url import URL
from crabs.options import Method

class Client:
    def __init__(self, url=None, data=None, method=None):
        self._session = Session()
        self._header = {}
        self._method = method
        self._url = url
        self._data = data
        self._resp = None

    def set_header(self, key, value):
        self._header[key] = value

    def set_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._header.update(headers)

    def _check_para(self, url=None, data=None):
        if url:  self._url = url
        if data: self._data = data

        if not self._url or not isinstance(self._url, URL):
            raise TypeError("URL required.")
        if self._data and not isinstance(self._data, dict):
            raise TypeError("Dict required.")

    def get(self, url=None, data=None):
        self._check_para(url, data)
        req = Request('GET', self._url.raw, data=self._data, headers=self._header)
        prepped = req.prepare()
        self._resp = self._session.send(prepped)

    def post(self, url=None, data=None):
        self._check_para(url, data)
        req = Request('POST', self._url.raw, data=self._data, headers=self._header)
        prepped = req.prepare()
        self._resp = self._session.send(prepped)

    @property
    def page(self):
        if self._resp is not None:
            return Page(self._resp.text, self._url)
        else:
            raise NotRespExp

    def _exec(self):
        if self._method == Method.GET:
            self.get()
        elif self._method == Method.GET:
            self.post()
        else:
            raise NotSuportMethodExp

    @property
    def status(self):
        if self._resp is None:
            self._exec()
        return self._resp.status_code

class NotRespExp(Exception):
    pass

class NotSuportMethodExp(Exception):
    pass