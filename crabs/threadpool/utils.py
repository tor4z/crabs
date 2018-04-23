import threading

class _Singleton:
    _SINGLETON_LOCK = threading.RLock()
    def __init__(self, _new=False):
        if not _new:
            raise Exception("Don't instancing it direct")

    def initialize(self, *args, **kwargs):
        pass
        
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(cls, "_LOCK"):
            with cls._SINGLETON_LOCK:
                if not hasattr(cls, "_LOCK"):
                    cls._LOCK = threading.RLock()
                
        if not hasattr(cls, "_INSTANCE"):
            with cls._LOCK:
                if not hasattr(cls, "_INSTANCE"):
                    cls._INSTANCE = cls(True)
                    cls._INSTANCE.initialize(*args, **kwargs)
        return cls._INSTANCE