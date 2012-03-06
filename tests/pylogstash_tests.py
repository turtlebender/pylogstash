from __future__ import absolute_import
import zmq
from threading import Thread
import logging
import json
from unittest import TestCase
import time
import sys

from zmq.utils.strtypes import asbytes
from pylogstash import LogstashHandler


class PyLogstashTest(TestCase):

    def setUp(self):
        self.sockets = []
        self.context = zmq.Context.instance()
        self.listener = zmq.Socket(self.context, zmq.SUB)
        self.listener.setsockopt(zmq.LINGER, 0)
        self.listener.setsockopt(zmq.SUBSCRIBE,asbytes(''))
        self.port = self.listener.bind_to_random_port("tcp://127.0.0.1")
        self.handler = LogstashHandler("tcp://127.0.0.1:{0}".format(self.port), context=self.context)
        self.handler.publisher.setsockopt(zmq.LINGER, 0)
        self.sockets.extend([self.listener, self.handler.publisher])
        time.sleep(0.1)

    def tearDown(self):
        contexts = set([self.context])
        while self.sockets:
            sock = self.sockets.pop()
            contexts.add(sock.context) # in case additional contexts are created
            sock.close(0)
        for ctx in contexts:
            t = Thread(target=ctx.term)
            t.daemon = True
            t.start()
            t.join(timeout=2)
            if sys.version[:3] == '2.5':
                t.is_alive = t.isAlive
            if t.is_alive():
                # reset Context.instance, so the failure to term doesn't corrupt subsequent tests
                zmq.core.context._instance = None
                raise RuntimeError("context could not terminate, open sockets likely remain in test")

    def test_basic_logging(self):
        log = logging.getLogger()
        log.addHandler(self.handler)
        log.setLevel(logging.DEBUG)
        log.info("hello")
        self.listener.recv()
