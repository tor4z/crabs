import unittest
from crabs.threadpool import (ThreadPool, 
                              ThreadPoolExecutor, 
                              Future)

class TestFuture(unittest.TestCase):
    def test_set_result(self):
        future = Future()
        future._set_result(1)
        self.assertTrue(future._done)

    def test_get_result(self):
        result = tuple(range(3))
        future = Future()
        future._set_result(result)
        self.assertEqual(future._get_result(), result)

    def test_wait(self):
        future = Future()
        self.assertFalse(future._wait(timeout=0.01))
        future._set_result(1)
        self.assertTrue(future._wait())
    def test_callback(self):
        class A:
            pass

        self._test_callback_flag = False
        for result in [1, "str", True, A()]:
            def f(n):
                self._test_callback_flag = True
                self.assertEqual(n, result)

            future = Future()
            future.add_callback(f)
            future._set_result(result)
            self.assertTrue(self._test_callback_flag)
            self._test_callback_flag = False
    
    def test_getattr(self):
        class A:
            def __init__(self, val):
                self.val = val

            def get_val(self):
                return self.val

        class B:pass

        for val in [100, "str", True, B()]:
            future = Future()
            future._set_result(A(val))

            self.assertEqual(future.val, val)
            self.assertEqual(future.get_val(), val)
    
    def test_str(self):
        class B:
            def __str__(self):
                return "B_class"

        for val in [100, "str", True, B()]:
            future = Future()
            future._set_result(val)
            self.assertEqual(str(future), str(val))
    
    def test_repr(self):
        class B:
            def __str__(self):
                return "B_class_str"
            def __repr__(self):
                return "B_class_repr"

        for val in [100, "str", True, B()]:
            future = Future()
            future._set_result(val)
            self.assertEqual(repr(future), repr(val))

import time
from crabs.threadpool.threadpool import ThreadPoolExp

def func(n):
    time.sleep(0.1)
    return n

class A:pass

class TestThreadPool(unittest.TestCase):
    def test_threadpool(self):
        args = [100, "str", True, A()]
        tp = ThreadPool(task_size=len(args))
        self.assertTrue(tp.task_empty)
        self.assertFalse(tp.task_full)
        self.assertEqual(tp.task_size, 0)
        for arg in args:
            future = tp.submit(func, arg)
            self.assertFalse(tp.task_full)
            self.assertEqual(future._get_result(), arg)

        tp.shutdown()
        with self.assertRaises(ThreadPoolExp):
            tp.submit(func, 1000)

    def test_put_task(self):
        args = [100, "str", True, A()]
        tp = ThreadPool(task_size=len(args))
        for arg in args:
            self.assertFalse(tp.task_full)
            future = tp._put_task((func, arg))

        self.assertFalse(tp.task_empty)
        self.assertTrue(tp.task_full)
        self.assertEqual(tp.task_size, len(args))
        self.assertEqual(tp.current_size, 0)

class TestThreadPoolExecutor(unittest.TestCase):
    def test_executor(self):
        args = [100, "str", True, A()]
        self._executor_flag = False
        with ThreadPoolExecutor() as e:
            for arg in args:
                def f(n):
                    self._executor_flag = True
                    self.assertEqual(n, arg)
                e.submit(f, arg)
                self._executor_flag = False
