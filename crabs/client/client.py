import requests
import urllib3
from http.cookiejar import CookieJar
from .response import Response

class Client:
    def __init__(self, headers, max_redirects=None):
        self._session = requests.Session()
        self._headers = headers
        self._max_redirects = max_redirects
        self._cookies = requests.utils.cookiejar_from_dict({})
        if self._max_redirects is not None:
            self._session.max_redirects = self._max_redirects

    def _update_req_headers(self, req):
        req.update_headers(self._headers)

    def _update_req_cookie(self, req):
        req.set_cookies(self._cookies)

    def _update_req(self, req):
        self._update_req_headers(req)
        self._update_req_cookie(req)

    def send(self, req):
        self._update_req(req)
        try:
            resp = self._session.send(req.prepare)
            self.update_cookies(resp.cookies)
            return Response(resp, req.url)
        except requests.ConnectionError:
            raise HttpConnError("Connect to {0} error.".format(req.url))
        except requests.exceptions.TooManyRedirects:
            raise ClientTooManyRedirects(
                "Exceeded {1} redirects for {1}".format(self._max_redirects ,req.url))
        except urllib3.exceptions.NewConnectionError as e:
            raise HttpConnError(e)
        except urllib3.exceptions.MaxRetryError as e:
            raise HttpConnError(e)
        


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

class NotSuportMethodExp(Exception):
    pass

class HttpError(Exception):
    pass

class ClientTooManyRedirects(Exception):
    pass