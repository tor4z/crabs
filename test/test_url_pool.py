import unittest
import random
from crabs.url_pool import URLPool
from crabs.http_client import URL
from crabs.options import Travel

class TestURLPool(unittest.TestCase):
    _url = "https://www.google.com/"
    _url2 = "https://map.google.com/"
    _url3 = "https://www.google.com.hk/"
    _url4 = "https://stackoverflow.com/"
    _url5 = """https://www.google.com.hk/search?newwindow=1&\
safe=active&source=hp&ei=tp_fWqbME8bx0ATl96uoCA&q=python&\
oq=python"""

    def test_size(self):
        pool = URLPool()
        count = random.randint(10, 20)
        for i in range(count):
            url = URL(self._url)
            pool.put_url(url)
        self.assertEqual(pool.size, count)

    def travel_mod(self):
        pool = URLPool()
        n = 10

        for i in range(n):
            url = URL(self._url, depth=1)
            pool.put_url(url)

        pool.set_treval_mod(Treval.BFS)
        url = pool.get_url()
        self.assertEqual(url.depth, 0)
        pool.set_treval_mod(Treval.DFS)
        url = pool.get_url()
        self.assertEqual(url.depth, n-1)

    def test_put_url(self):
        pool = URLPool()
        pool.put_url(self._url)
        url = pool.get_url()

        self.assertTrue(isinstance(url, URL))
        self.assertEqual(url.raw, self._url)
        self.assertEqual(url.depth, 0)

    def test_clear(self):
        pool = URLPool()
        count = random.randint(10, 20)
        for i in range(count):
            url = URL(self._url)
            pool.put_url(url)
        pool.clear()
        self.assertEqual(pool.size, 0)

    def test_allow_netloc_filter(self):
        pool = URLPool()
        pool.set_allow_netloc(["*.google.com"])
        pool.put_url(self._url)
        pool.put_url(self._url2)
        pool.put_url(self._url3)
        pool.put_url(self._url4)
        self.assertEqual(pool.size, 3)
        
        pool = URLPool()
        pool.set_allow_netloc(["*.google.com$"])
        pool.put_url(self._url)
        pool.put_url(self._url2)
        pool.put_url(self._url3)
        pool.put_url(self._url4)
        self.assertEqual(pool.size, 2)

        pool = URLPool()
        pool.set_allow_netloc(["*.google.*"])
        pool.put_url(self._url)
        pool.put_url(self._url2)
        pool.put_url(self._url3)
        pool.put_url(self._url4)
        self.assertEqual(pool.size, 3)
        

        pool = URLPool()
        pool.set_allow_netloc(["www.google.*"])
        pool.put_url(self._url)
        pool.put_url(self._url2)
        pool.put_url(self._url3)
        pool.put_url(self._url4)
        self.assertEqual(pool.size, 2)
        
        pool = URLPool()
        pool.set_allow_netloc(["*.microsoft.*"])
        pool.put_url(self._url)
        pool.put_url(self._url2)
        pool.put_url(self._url3)
        pool.put_url(self._url4)
        self.assertEqual(pool.size, 0)

    def test_disallow_path_filter(self):
        pool = URLPool()
        pool.set_disallow_path(["/search*"])
        pool.put_url(self._url)
        pool.put_url(self._url2)
        pool.put_url(self._url3)
        pool.put_url(self._url4)
        pool.put_url(self._url5)
        self.assertEqual(pool.size, 4)

    