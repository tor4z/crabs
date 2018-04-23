from urllib.parse import urlsplit, urljoin
import json
from .options import TextType
from .parser import HTMLParser

class Response:
    def __init__(self, resp, url):
        self._url = url
        self._resp = resp
        self._text = None
        self._json = None
        self._is_json = True
        self._ok = None
        self._text_type = None
        self._html = None
        self._depth = self._url.depth
        self._status = None
        self._reason = None
        self._close = False
        self.close()

    @property
    def text(self):
        if self._text is None:
            self._text = self._resp.text
        return self._text

    @property
    def is_json(self):
        return self._is_json and self.json is not None

    @property
    def json(self, **kwargs):
        if self._json is None and self._is_json:
            try:
                self._json = self._resp.json(**kwargs)
                self._is_json = True
            except json.decoder.JSONDecodeError:
                self._is_json = False
        return self._json

    @property
    def ok(self):
        if self._ok is None:
            self._ok = self._resp.ok
        return self._ok

    @property
    def url(self):
        return self._url

    @property
    def text_type(self):
        if self._text_type is None:
            if self.is_json:
                self._text_type = TextType.JSON
            else:
                self._text_type = TextType.HTML
        return self._text_type

    @property
    def depth(self):
        return self.url.depth

    @property
    def status(self):
        if self._status is None:
            if self._resp is None:
                raise NotResponseExp
            self._status = self._resp.status_code
        return self._status

    @property
    def reason(self):
        if self._reason is None:
            self._reason = self._resp.reason
        return self._reason

    @property
    def html(self):
        if self._html is None:
            if self.text_type == TextType.HTML:
                self._html = HTMLParser(self.text, self.url)
            else:
                raise TypeError("{0} is not a html page.".format(self.url))
        return self._html

    def _before_close(self):
        self.text
        self.json
        self.ok
        self.status
        self.reason

    def close(self):
        if not self._close:
            self._before_close()
            self._resp.close()
            self._close = True

class NotResponseExp(Exception):
    pass
