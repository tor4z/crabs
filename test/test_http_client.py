import unittest
from crabs.http_client import Client, Request, Response
from crabs.http_client.request import NotSuportMethod
from crabs.http_client.options import Method
from crabs.http_client.utils import ClientHeaders
from crabs.http_client.url import URL

_url = "https://www.google.com/search?q=python"

class TestRequest(unittest.TestCase):
    def test_new_request(self):
        with self.assertRaises(NotSuportMethod):
            Request("PUT", URL(_url), data=None, headers={})
        with self.assertRaises(TypeError):
            Request(Method.GET, _url, data=None, headers={})
        with self.assertRaises(TypeError):
            Request(Method.GET, URL(_url), data=("key", "value"), headers={})
        with self.assertRaises(TypeError):
            Request(Method.GET, URL(_url), data=None, headers=("Host", "www.google.com"))
        req = Request(Method.GET, URL(_url))
        self.assertTrue(req.ready)

    def test_update_headers(self):
        headers = ClientHeaders
        req = Request(Method.GET, URL(_url))
        req.update_headers(headers)
        req_headers = req._headers
        for key in headers:
            self.assertIn(key, req_headers.keys())
            self.assertEqual(req_headers[key], headers[key])

    def random_str(self, n):
        return "".join(choices("abcdefghijklmnopqrstuvwxyz0123456789", k=i))

    def test_set_cookies(self):
        from requests.utils import cookiejar_from_dict
        from requests.utils import dict_from_cookiejar
        from random import choices, randint
        n = 10
        cookie_dict = {}

        for i in range(n):
            key = self.random_str(i+1)
            value = self.random_str(i+1) if i % 2 else i
            cookie_dict[key] = value

        cookies = cookiejar_from_dict(cookie_dict)
        req = Request(Method.GET, URL(_url))
        req.set_cookies(cookies)
        req_cookies = req._cookies
        req_cookies_dict = dict_from_cookiejar(req_cookies)

        for key in cookie_dict:
            self.assertIn(key, req_cookies_dict.keys())
            self.assertEqual(req_cookies_dict[key], cookie_dict[key])

    def test_url(self):
        url = URL(_url)
        req = Request(Method.GET, url)
        self.assertEqual(req.url, url)

class TestResponse(unittest.TestCase):
    pass

class TestClient(unittest.TestCase):
    pass
