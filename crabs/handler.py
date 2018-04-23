import re, json
from .client.url import URL
from .client.request import Request
from .client.client import NotSuportMethodExp, HttpError
from .options import Method

class Handler:
    def __init__(self, url, method, crabs):
        if not isinstance(url, URL):
            raise TypeError
        self.url = url
        self.method = method
        self._headers = {}
        self._data = None
        self._crabs = crabs
        self.settings()

    def set_header(self, key, value):
        self._headers[key] = value

    def set_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._headers.update(headers)

    def set_data(self, data):
        if not isinstance(data, dict):
            raise TypeError("Dict required.")
        self._data = data

    @property
    def _resp(self):
        req = Request(self.method, self.url, 
                    self._data, self._headers)
        resp = self._crabs.client.send(req)
        return resp
    
    def execute(self):
        if not self._resp.ok:
            raise HttpError("[{0}] {1}".format(self._resp.status, self._resp.reason))
        if self.method == Method.GET:
            self.get(self._resp)
        elif self.method == Method.POST:
            self.post(self._resp)
        else:
            raise NotSuportMethodExp
        return self._resp

    def settings(self):
        """
        Set headers, data here
        """
        pass

    def get(self, resp):
        pass

    def post(self, resp):
        pass

class DefaultHandler(Handler):
    def __init__(self, url, method, crabs):
        super().__init__(url, method, crabs)