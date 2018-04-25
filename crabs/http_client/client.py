import requests
import urllib3
from http.cookiejar import CookieJar
from .response import Response
from .utils import ClientHeaders
from .url import URL
from .request import Request

class Client:
    def __init__(self, headers=None, max_redirects=None, html_parser=None):
        self._session = requests.Session()
        self._headers = headers or ClientHeaders
        self._max_redirects = max_redirects
        self._html_parser = html_parser
        self._cookies = requests.utils.cookiejar_from_dict({})
        self._statistics = {
            "Total": 0,
            "Succeed": 0,
            "Failed": 0
        }

    @property
    def report(self):
        self._statistics["Failed"] = self._statistics["Total"] - self._statistics["Succeed"]
        report = "Http:"
        for key in self._statistics:
            report += "{0}({1})".format(key, self._statistics[key])
        return report

    def set_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._headers = headers

    def set_html_parser(self, html_parser):
        if html_parser is not None:
            self._html_parser = html_parser

    def update_headers(self, headers):
        if headers is not None:
            if not isinstance(headers, dict):
                raise TypeError("Dict required.")
            self._headers.update(headers)
    
    def set_max_redirects(self, max_redirects):
        if max_redirects is not None:
            if max_redirects < 1:
                raise ValueError("Max redirects should be greater than 0.")
            self._max_redirects = max_redirects
            self._session.max_redirects = self._max_redirects

    def _update_req_headers(self, req):
        req.update_headers(self._headers)

    def _update_req_cookies(self, req):
        req.set_cookies(self.cookies)

    def _update_req(self, req):
        self._update_req_headers(req)
        self._update_req_cookies(req)

    def get(self, url, data=None):
        req = Request("GET", URL(url), data)
        return self.send(req)

    def post(self, url, data=None):
        req = Request("POST", URL(url), data)
        return self.send(req)

    def send(self, req):
        self._update_req(req)
        try:
            resp = self._session.send(req.prepare)
            self.update_cookies(resp.cookies)
            resp = Response(resp, req.url, self._html_parser)
            if resp.ok:
                self._statistics["Succeed"] += 1
            return resp
        except requests.ConnectionError:
            raise HttpConnError("Connect to {0} error.".format(req.url))
        except requests.exceptions.TooManyRedirects:
            raise ClientTooManyRedirects(
                "Exceeded {1} redirects for {1}".format(self._max_redirects ,req.url))
        except urllib3.exceptions.NewConnectionError as e:
            raise HttpConnError(e)
        except urllib3.exceptions.MaxRetryError as e:
            raise HttpConnError(e)
        finally:
            self._statistics["Total"] += 1

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