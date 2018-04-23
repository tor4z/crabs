import threading
from queue import Queue
import os
from .utils import _Singleton

class Future:
    def __init__(self):
        self._result_ = None
        self._event = threading.Event()
        self._has_callback = False
        self._callback_func = None
        self._done=False

    def _set_result(self, result):
        self._result_ = result
        self._done = True
        self._event.set()

    def _get_result(self, *args):
        self._wait(*args)
        return self._val

    def _wait(self, *args):
        if not self._event.is_set():
            self._event.wait(*args)

    @property
    def _result(self):
        return self.get_result()

    def add_callback(self, func):
        self._has_callback = True
        if not callable(func):
            raise TypeError("Callback should be callable.")
        self._callback_func = func

    def _callback(self):
        if self._has_callback:
            self._callback_func(self._result)

    def __delattr__(self, name):
        raise FutureExp("This object cann't delete attribute.")

    def __setattr__(self, name, value):
        raise FutureExp("This object cann't set attribute.")

    def __getattr__(self, name):
        if hasattr(self._result, name):
            return getattr(self._result, name)
        else:
            raise FutureExp("No attribute named ({0}).".format(name))

    def __str__(self):
        return self._result
        
    def __repr__(self):
        return self.__str__()

class _Thread(threading.Thread):
    def __init__(self, thread_pool, name=None):
        self._name = name
        self._thread_pool = thread_pool
        super().__init__(name=self._name)

    def run(self):
        while True:
            task = self._thread_pool.get_task(block=True)
            if task is not None:
                func, args, kwargs, future = task
                result = func(*args, **kwargs)
                future._set_result(result)
            else:
                self._thread_pool.put_task(None)
                return
                
class ThreadPool:
    def __init__(self, max_size=None, queue_cls=None):
        if max_size is None:
            max_size = ((os.cpu_count() or 1) * 5)
        self._max_size = max_size
        if self._max_size < 1:
            raise ValueError("ThreadPool max size must be greater or equal than 1.")
        self._pool = []
        if queue_cls is None:
            queue_cls = Queue
        self._queue = queue_cls()
        self._shutdown_lock = threading.RLock()
        self._shutdown = False
        self._queue_lock = threading.RLock()

    @property
    def current_size(self):
        return len(self._pool)

    def get_task(self, *args):
        with self._queue_lock:
            task =  self._queue.get(*args)
        return task

    def put_task(self, task):
        with self._queue_lock:
            self._queue.put(task)

    def _shutdown_checker(self):
        if self._shutdown:
            raise ThreadPoolExp("ThreadPool already shutdown.")

    def submit(self, func, *args, **kwargs):
        self._shutdown_checker()
        future = Future()
        with self._queue_lock:
            self._queue.put((func, *args, **kwargs, future))
        return future

    def _new_thread(self):
        self._shutdown_checker()
        if self._max_size <= self.current_size:
            t = threading.Thread(target=_worker, args=(self._queue))
            t.setDaemon(True)
            t.start()
            self._pool.append(t)

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
            self.put_task(None)
        if wait:
            for t in self._pool:
                t.join()

class ThreadPoolExecutor:
    def __init__(self, max_size=None, queue_cls=None):
        self._threadpool = ThreadPool(max_size=max_size, queue_cls=queue_cls)

    def __enter__(self):
        pass

    def __exit__(self, ex_type, ex_value, traceback):
        self._threadpool.shutdown()

    def submit(self, func, *args, **kwargs):
        return self._threadpool.submit(func, *args, **kwargs)

class StaticThreadPoolExecutor(_Singleton, ThreadPoolExecutor):
    def __init__(self):
        _Singleton.__init__(self)

    def _initialize(self, max_size=None, queue_cls=None):
        ThreadPoolExecutor.__init__(self, max_size=max_size, queue_cls=queue_cls)

class FutureExp(Exception):
    pass

class ThreadExp(Exception):
    pass

class ThreadPoolExp(Exception):
    pass