import re
from bs4 import BeautifulSoup
from apiwatcherlink.utils.text import split80


def gettitle(html):
    bs = BeautifulSoup(html, 'html.parser')
    if bs:
        title = bs.find('title').text
        return title
    else:
        return ""


def cleanhtml(html):
    def clear(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', unicode(element)):
            return False
        elif re.match('<!.*', unicode(element)):
            return False
        return True

    bs = BeautifulSoup(html, 'html.parser')
    body = filter(clear, bs.find_all(text=True))
    cleanh = []
    for line in body:
        linestrip = re.sub(' +', ' ', "".join(line.replace('\n', '').replace('\t', '')))
        lenlinestrip = len(linestrip)
        if lenlinestrip > 0 and linestrip != '' and linestrip != ' ':
            if lenlinestrip > 80:
                for l in split80(linestrip):
                    cleanh.append("%s" % l)
            else:
                cleanh.append("%s" % linestrip)
    return cleanh