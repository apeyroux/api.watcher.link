# coding=utf-8

#todo: faire des snap?get ?make ?list

import datetime
from difflib import SequenceMatcher, HtmlDiff

import requests
from mongoengine import DoesNotExist, ValidationError
from flask import Flask, request, jsonify, abort, Response
from bs4 import BeautifulSoup
from selenium import webdriver
from flask.ext.mongoengine import MongoEngine
from mongoengine.fields import StringField, DateTimeField, ListField, ReferenceField, FloatField, BinaryField
from utils.text import cleanhtml

DEFAULTMAXRATION = 0.97

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "api-watcher-link"
}

db = MongoEngine(app)


# Pour plustard, sert à faire un "cache" de diff
class Diff(db.Document):
    pass


class Snap(db.Document):
    html = StringField()
    dthr = DateTimeField()
    screen = BinaryField()


class Page(db.Document):
    name = StringField(required=True)
    baseurl = StringField(required=True)
    maxratio = FloatField()
    snaps = ListField(ReferenceField(Snap))
    diffs = ListField(ReferenceField(Diff))


@app.route('/getsnap/<snapid>/')
def getsnap(snapid):
    try:
        snap = Snap.objects.get(id=snapid)
    except DoesNotExist:
        abort(404)
    except ValidationError:
        abort(500)
    except:
        abort(500)
    else:
        return jsonify({'snap': snap.to_json()})


@app.route('/diffhtml/<pageid>/')
def diffhtml(pageid):
    d = HtmlDiff()
    try:
        snaps = Page.objects.get(id=pageid).snaps
    except DoesNotExist:
        abort(404)
    except ValidationError:
        abort(500)
    except:
        abort(500)
    else:
        if len(snaps) > 2:
            fst = snaps[-1]
            snd = snaps[-2]
            return d.make_file(cleanhtml(snd.html), cleanhtml(fst.html))
        else:
            abort(500)


@app.route('/diff/<pageid>/')
@app.route('/diff/<snapa>/<snapb>/')
def diff(pageid=None, snapa=None, snapb=None):
    if pageid:
        try:
            snaps = Page.objects.get(id=pageid).snaps
        except DoesNotExist:
            abort(404)
        except ValidationError:
            abort(500)
        except:
            abort(500)
        else:
            if len(snaps) >= 2:
                fst = snaps[-1]
                snd = snaps[-2]
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
                        txtreplace.append(
                            ("%s <-> %s" % ("".join(fstcleanhtml[i1:i2]), "".join(sndcleanhtml[j1:j2]))).strip())
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
    elif snapa and snapb:
        try:
            sa = Snap.objects.get(id=snapa)
            sb = Snap.objects.get(id=snapb)
        except DoesNotExist:
            abort(404)
        except ValidationError:
            abort(500)
        except:
            abort(500)
        else:
            fstcleanhtml = cleanhtml(sa.html)
            sndcleanhtml = cleanhtml(sb.html)
            sm = SequenceMatcher(None,
                                 sndcleanhtml,
                                 fstcleanhtml)
            txtinsert = []
            txtdel = []
            txtreplace = []
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "replace":
                    txtreplace.append(
                        ("%s <-> %s" % ("".join(fstcleanhtml[i1:i2]), "".join(sndcleanhtml[j1:j2]))).strip())
                if tag == "insert":
                    txtinsert.append(("%s %s" % ("".join(fstcleanhtml[i1:i2]), "".join(sndcleanhtml[j1:j2]))).strip())
                if tag == "delete":
                    txtdel.append(("%s %s" % ("".join(fstcleanhtml[i1:i2]), "".join(sndcleanhtml[j1:j2]))).strip())
            return jsonify({
                'diff': {'fst': {'id': str(sa.id), 'dthr': sa.dthr},
                         'snd': {'id': str(sb.id), 'dthr': sb.dthr},
                         'ratio': sm.ratio(),
                         'insert': txtinsert,
                         'replace': txtreplace,
                         'delete': txtdel}
            })
    else:
        abort(500)

@app.route('/snap/<pageid>/')
def snap(pageid):
    try:
        page = Page.objects.get(id=pageid)
    except DoesNotExist:
        abort(404)
    except ValidationError:
        abort(500)
    except:
        abort(500)
    else:
        html = requests.get(page.baseurl).text
        phantom = webdriver.PhantomJS(desired_capabilities={'acceptSslCerts': True},
                                      service_args=['--web-security=false',
                                                    '--ssl-protocol=any',
                                                    '--ignore-ssl-errors=true'])
        phantom.set_window_size(1024, 768)
        phantom.get(page.baseurl)
        screenshot = phantom.get_screenshot_as_png()
        page.update(push__snaps=Snap(html, datetime.datetime.now(), screenshot).save())
        phantom.close()
        return jsonify({'page': page})


@app.route('/screen/<snapid>/')
def screen(snapid):
    try:
        snap = Snap.objects.get(id=snapid)
    except DoesNotExist:
        abort(404)
    except ValidationError:
        abort(500)
    except:
        abort(500)
    else:
        return Response(snap.screen, mimetype="image/png")


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
                page = Page(name, url, DEFAULTMAXRATION)
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
