import logging
import zmq
import socket
import datetime


class Handler(logging.Handler):
    """ A logging handler for sending notifications to a 0mq PUSH.
    """
    def __init__(self, connect_string='tcp://127.0.0.1:2120', fields=[], type=None, context=None):
        logging.Handler.__init__(self)
        self._context = context if context is not None else zmq.Context()
        self.fields = fields
        self.type = type
        self.pub = self._context.socket(zmq.PUB)
        self.pub.connect(connect_string)

    def emit(self, record):
        field_dict = {}
        for field in self.fields:
            field_dict[field] = getattr(record, field)
        field_dict['timestamp'] = datetime.datetime.fromtimestamp(record.created).isoformat()
        host = socket.gethostname()
        message = {
            "@source": record.filename,
            "@tags": ["pylogstash"],
            "@type": self.type,
            "@fields": field_dict,
            "@source_host": host,
            "@message": self.format(record)
        }
        self.pub.send_json(message)


log = logging.getLogger()
log.addHandler(Handler(type="graph", fields=['levelname', 'filename', 'module', 'args', 'pathname']))
log.warn("Test")
