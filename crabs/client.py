from requests import Request, Session
from crabs.page import Page

class Client:
    def __init__(self):
        self._session = Session()
        self._header = {}
        self._resp = None
        self._url = None

    def set_header(self, key, value):
        self._header[key] = value

    def get(self, url, data=None):
        self._url = url
        req = Request('GET', url, data=data, headers=self._header)
        prepped = req.prepare()
        self._resp = self._session.send(prepped)

    def post(self, url, data=None):
        self._url = url
        req = Request('POST', url, data=data, headers=self._header)
        prepped = req.prepare()
        self._resp = self._session.send(prepped)

    @property
    def page(self):
        if self._resp is not None:
            return Page(self._resp.text, self._url)
        else:
            raise NotRespExp

class NotRespExp(Exception):
    pass