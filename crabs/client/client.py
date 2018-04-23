import requests
from http.cookiejar import CookieJar
from .response import Response

class Client:
    def __init__(self, headers):
        self._session = requests.Session()
        self._headers = headers
        self._cookies = requests.utils.cookiejar_from_dict({})
        
    def _update_req_headers(self, req):
        req.update_headers(self._headers)

    def _update_req_cookie(self, req):
        req.set_cookies(self._cookies)

    def _update_req(self, req):
        self._update_req_cookie(req)
        self._update_req_cookie(req)

    def send(self, req):
        req = self._update_req(req)
        try:
            resp = self._session.send(req.prepped)
            self.update_cookies(resp.cookies)
            return Response(resp, req.url)
        except requests.ConnectionError:
            raise HttpConnError("Connect to {0} error.".format(prepped.url))

    def update_cookies(self, cookies):
        """
        Cookies is CookieJar type
        """
        self._cookies = requests.cookies.merge_cookies(self._cookies, cookies)

    @property
    def cookies(self):
        """
        Cookies is CookieJar type
        """
        return self._cookies
    
class HttpConnError(Exception):
    pass

class NotRespExp(Exception):
    pass
