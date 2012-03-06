from __future__ import absolute_import
import zmq
import multiprocessing
import logging
from pylogstash import LogstashHandler


def subscribe(queue):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://127.0.0.1:22222")
    socket.setsockopt(zmq.SUBSCRIBE, "")
    queue.put(socket.recv())


def test():
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=subscribe, args=(queue, ))
    process.start()

    log = logging.getLogger()
    handler = LogstashHandler()
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    log.warn("hello")
    process.join()
    import json
    message = json.loads(queue.get())
    assert message['@message'] == "hello"


if __name__ == "__main__":
    test()
