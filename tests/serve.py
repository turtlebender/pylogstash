from __future__ import absolute_import
import zmq
import multiprocessing
import logging
from pylogstash import LogstashHandler
import unittest


def subscribe():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://127.0.0.1:2120")
    socket.setsockopt(zmq.SUBSCRIBE, "")

    print(socket.recv())


class PylogstashTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        process2 = multiprocessing.Process(target=subscribe)
        process2.start()

        log = logging.getLogger()
        handler = LogstashHandler()
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        log.warn("hello")

PylogstashTest().test()
