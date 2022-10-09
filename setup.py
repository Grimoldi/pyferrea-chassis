from setuptools import setup
from .chassis import __version__


if __name__ == "__main__":
    setup(
        name='ferrea-chassis',
        version=__version__,
        description="Python module for observability of the Ferrea application",

        url='https://github.com/Grimoldi/pyferrea-chassis',
        author='Eugenio Grimoldi',
        author_email='',

        py_modules=['chassis'],
        install_requires=[
            'logging',
            'logstash_formatter',
            'statsd',
        ],
        setup_requires=[
            'logging',
            'logstash_formatter',
            'statsd',
        ]
    )