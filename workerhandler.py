# -*- coding: utf-8 -*-
"""
Derived queueing and threading handler class from Python
standard modules 'queue' and 'threading'.

Some methods are overriden to help wildcat perform its tasks.

Some methods added to support queueing and threading.
"""
import queue
from time import time

"""
Queueing

"""

class WildcatQueue(queue.Queue):
    """
    Reimplementation of Python Queue class to support WildCat's needs and operations.
    """

    def __init__(self, maxsize = 0):
        super(WildcatQueue, self).__init__(maxsize)

    def get(self, block=False, timeout=None):
        '''Remove and return an item from the queue.

        If optional args 'block' is True and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).

        Override : Return default string "Empty" instead of rising Empty error
                    or wait until the queue gets new items.

                    block = False by default.
        '''
        with self.not_empty:
            if not block:
                if not self._qsize():
                    #raise Empty
                    return "Empty"
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = time() + timeout
                while not self._qsize():
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        #raise Empty
                        return "Empty"
                    self.not_empty.wait(remaining)
            item = self._get()
            self.not_full.notify()
            return item

"""
Threading
"""
def terminate_all_threads(thread_list):
    """Wait for all threads in threadList to terminate"""
    [t.join() for t in thread_list if t.is_alive()]
