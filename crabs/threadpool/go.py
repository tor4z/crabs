from .threadpool import DefaultThreadPool

class go:
    def __init__(self, func):
        self._func = func

    @property
    def _threadpool(self):
        return DefaultThreadPool.instance()

    def __call__(self, *args, **kwargs):
        future = self._threadpool.submit(self._func, *args, **kwargs)
        return future