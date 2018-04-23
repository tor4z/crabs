import requests
from http.cookiejar import CookieJar
from .response import Response
from .url import URL
from .options import Method

class Request:
    def __init__(self, method, url, data, headers):
        self._headers = headers
        self._prepare = None
        self._url = url
        self._data = data
        self._method = method
        self._cookies = None

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
        self._headers["Referer"] = self._url.netloc

    @property
    def prepare(self):
        if self._prepare is None:
            self._set_header()
            req = requests.Request(method = self._method, 
                                    url = self._url.raw, 
                                    data = self._data, 
                                    cookies = self._cookies,
                                    headers = self._header)
            self._prepare = req.prepare()
        return self._prepare

    @property
    def url(self):
        return self._url