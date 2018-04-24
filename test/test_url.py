import unittest
from crabs.client import URL

class TestURL(unittest.TestCase):
    _netloc = "www.host.com"
    _scheme = "https"
    _url = "https://www.host.com"
    _path = "/some/path"
    _query = {"a":1, "b":2}
    _query_string = "a=1&b=2"

    @property
    def url(self):
        return URL(self._url, self._path)

    def test_depth(self):
        url = self.url
        self.assertEqual(url.depth, 0)
        url.insc_depth()
        self.assertEqual(url.depth, 1)
        url.desc_depth()
        self.assertEqual(url.depth, 0)

    def test_path(self):
        url = self.url
        self.assertEqual(url.path, self._path)
        path = "/aaa/bbb"
        url.set_path(path)
        self.assertEqual(url.path, path)
        self.assertEqual(url.raw, self._url+path)

    def test_netloc(self):
        self.assertEqual(self.url.netloc, self._netloc)

    def test_host(self):
        self.assertEqual(self.url.host, self._url+"/")

    def test_scheme(self):
        self.assertEqual(self.url.scheme, self._scheme)

    def test_query(self):
        path = "/path?a=1&b=2"
        d = {"a":"1", "b":"2"}
        url = URL(self._url, path)
        self.assertEqual(url.query, d)

    def test_urljoin(self):
        target = "http://www.aaa.com/bbb"
        origin = "http://www.aaa.com/aaa"
        self.assertEqual(URL.urljoin(origin, target), target)
        self.assertEqual(URL.urljoin(origin, "/bbb"), target)

    def test_query_str(self):
        url = self.url
        url.set_query(self._query)
        self.assertEqual(url.query_str, self._query_string)
        path = "/path?a=1&b=2"
        url = URL(self._url, path)
        self.assertEqual(url.query_str, "a=1&b=2")
    
    def test_dict_to_qs(self):
        self.assertEqual(URL.dict_to_qs(self._query), self._query_string)

    def test_path_query(self):
        url = self.url
        url.set_path(self._path)
        url.set_query(self._query)
        self.assertEqual(url.path_query, self._path + "?" + 
                        self._query_string)

    def test_is_full_url(self):
        url1 = "http://www.aaa.com/path?sdsd=ss"
        url2 = "/path?uu=11"
        self.assertTrue(URL.is_full_url(url1))
        self.assertFalse(URL.is_full_url(url2))