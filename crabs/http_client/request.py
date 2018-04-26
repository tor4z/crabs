import requests
from http.cookiejar import CookieJar
from .response import Response
from .url import URL
from .options import Method

class Request:
    def __init__(self, method, url, data=None, headers={}):
        if not isinstance(url, URL):
            raise TypeError("URL required.")
        if not method in Method.ALL:
            raise NotSuportMethod("{0} method is not suported.".format(method))
        if data is not None and not isinstance(data, dict):
            raise TypeError("Dict required.")
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._headers = headers
        self._prepare = None
        self._url = url
        self._data = data
        self._method = method
        self._cookies = None

    @property
    def ready(self):
        return self._url is not None and\
                self._method is not None

    def update_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        headers.update(self._headers)
        self._headers = headers

    def set_cookies(self, cookies):
        if not isinstance(cookies, CookieJar):
            raise TypeError("CookieJar required.")
        self._cookies = cookies

    def _set_header(self):
        self._headers["Host"] = self._url.netloc
        self._headers["Referer"] = self._url.host
        self._headers["Origin"] = self._url.host

    @property
    def prepare(self):
        self._set_header()
        req = requests.Request(method = self._method, 
                                url = self._url.raw, 
                                data = self._data, 
                                cookies = self._cookies,
                                headers = self._headers)
        return req.prepare()

    @property
    def url(self):
        return self._url

class NotSuportMethod(Exception):
    pass