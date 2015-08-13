from distutils.core import setup

setup(
    name='api.watcher.link',
    version='0.1',
    packages=[''],
    url='http://api.watcher.link',
    license='',
    author='ja',
    author_email='m@ja.pe',
    description='', requires=['flask',
                              'requests',
                              'mongoengine',
                              'beautifulsoup4',
                              'selenium']
)
