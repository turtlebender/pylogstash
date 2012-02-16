
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Logging hander to ship logs to logstash via zmq',
    'author': 'Tom Howe',
    'url': 'https://github.com/turtlebender/pylogstash',
    'download_url': 'Where to download it.',
    'author_email': 'turtlebender@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'pyzmq'],
    'packages': ['pylogstash'],
    'scripts': [],
    'name': 'pylogstash'
}

setup(**config)
