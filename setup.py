from distutils.core import setup

setup(
    name='api.watcher.link',
    version='0.1',
    packages=['apiwatcherlink', 'apiwatcherlink.model', 'apiwatcherlink.rest', 'apiwatcherlink.utils'],
    url='http://api.watcher.link',
    license='',
    author='ja',
    author_email='m@ja.pe',
    scripts=['scripts/apiwatcherlink'],
    description='',
    requires=['flask',
              'requests',
              'mongoengine',
              'beautifulsoup4',
              'selenium']
)
