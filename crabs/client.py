from requests import Request, Session

class Client:
    def __init__(self):
        self._session = Session()
        self._header = {}
        self._resp = None

    def set_header(self, key, value):
        self._header[key] = value

    def get(self, url, data=None):
        req = Request('GET', url, data=data, headers=self._header)
        prepped = req.prepare()
        self._resp = self._session.send(prepped)

    def post(self, url, data=None):
        req = Request('POST', url, data=data, headers=self._header)
        prepped = req.prepare()
        self._resp = self._session.send(prepped)

    @property
    def text(self):
        if self._resp is not None:
            return self._resp.text