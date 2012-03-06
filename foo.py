from pylogstash import LogstashHandler
import logging
handler = LogstashHandler()
log = logging.getLogger()
log.addHandler(handler)
log.warn("foo")
