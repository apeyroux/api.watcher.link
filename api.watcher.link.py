# coding=utf-8
import datetime
import re

import requests
from flask import Flask, request, jsonify, abort
from bs4 import BeautifulSoup

# import weasyprint # plustard, faire un screen de la page
from difflib import SequenceMatcher, HtmlDiff
from flask.ext.mongoengine import MongoEngine
from mongoengine.fields import StringField, DateTimeField, ListField, ReferenceField

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "db": "api-watcher-link"
}

db = MongoEngine(app)

# Pour plustard, sert à faire un "cache" de diff
class Diff(db.Document):
    pass


class Content(db.Document):
    html = StringField()
    dthr = DateTimeField()


class Page(db.Document):
    name = StringField(required=True)
    baseurl = StringField(required=True)
    contents = ListField(ReferenceField(Content))
    diffs = ListField(ReferenceField(Diff))


def split80(tbl):
    lentbl = len(tbl)
    if lentbl >= 80:
        yield "".join(list(split80(tbl[80:]))[:80])
    else:
        yield tbl


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


@app.route('/content/<contentid>/')
def content(contentid):
    content = Content.objects.get(id=contentid)
    return jsonify({'content': content.to_json()})


@app.route('/diffhtml/<pageid>/')
def diffhtml(pageid):
    d = HtmlDiff()
    contents = Page.objects.get(id=pageid).contents
    if len(contents) > 2:
        fst = contents[-1]
        snd = contents[-2]
        return d.make_file(cleanhtml(snd.html), cleanhtml(fst.html))
    else:
        abort(500)


@app.route('/diff/<pageid>/')
def diff(pageid):
    contents = Page.objects.get(id=pageid).contents
    if len(contents) >= 2:
        fst = contents[-1]
        snd = contents[-2]
        fstcleanhtml = cleanhtml(fst.html)
        sndcleanhtml = cleanhtml(snd.html)
        sm = SequenceMatcher(None,
                             sndcleanhtml,
                             fstcleanhtml)
        txtinsert = []
        txtdel = []
        txtreplace = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "replace":
                txtreplace.append(("%s <-> %s" % ("".join(fstcleanhtml[i1:i2]), "".join(sndcleanhtml[j1:j2]))).strip())
            if tag == "insert":
                txtinsert.append(("%s %s" % ("".join(fstcleanhtml[i1:i2]), "".join(sndcleanhtml[j1:j2]))).strip())
            if tag == "delete":
                txtdel.append(("%s %s" % ("".join(fstcleanhtml[i1:i2]), "".join(sndcleanhtml[j1:j2]))).strip())
        return jsonify({
            'diff': {'fst': {'id': str(fst.id), 'dthr': fst.dthr},
                     'snd': {'id': str(snd.id), 'dthr': snd.dthr},
                     'ratio': sm.ratio(),
                     'insert': txtinsert,
                     'replace': txtreplace,
                     'delete': txtdel}
        })
    else:
        abort(500)


@app.route('/snap/<pageid>/')
def snap(pageid):
    page = Page.objects.get(id=pageid)
    html = requests.get(page.baseurl).text
    page.update(push__contents=Content(html, datetime.datetime.now()).save())
    return jsonify({'page': page})


@app.route('/new/')
def new():
    url = request.args['url']
    js = {'page': None}
    if url:
        try:
            html = requests.get(url).text
            bs = BeautifulSoup(html, 'html.parser')
            name = bs.find('title').text
            page = Page.objects(name=name)
            if page:
                js['page'] = page
                return jsonify(js)
            else:
                page = Page(name, url)
                page.save()
                # todo: init des snap, c'est moche ...
                for _ in range(0, 2):
                    snap(page.id)
                js['page'] = page
                return jsonify(js)
        except:
            abort(500)
    else:
        abort(500)


@app.route('/')
def main():
    return jsonify({'api': '1.0'})


if __name__ == '__main__':
    app.run("0.0.0.0", port=5050, debug=True)
