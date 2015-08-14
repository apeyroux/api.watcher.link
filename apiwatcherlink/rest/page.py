from flask.views import MethodView
from flask import request, abort, Response, jsonify
import requests
import datetime
from apiwatcherlink.model.page import Page
from apiwatcherlink import DEFAULTMAXRATION
from apiwatcherlink.utils.web import gettitle


def page2js(page):
    js = {'page': {'id': "%s" % page.id,
                   'name': page.name,
                   'baseurl': page.baseurl,
                   'maxratio': page.maxratio,
                   'snaps': [{'dthr': snap.dthr, 'id': "%s" % snap.id} for snap in page.snaps]}}
    return jsonify(js)


class PageView(MethodView):
    def get(self, id):
        page = Page.objects.get_or_404(id=id)
        return page2js(page)

    def post(self):
        url = request.values['url']
        if not url:
            abort(400)
        try:
            html = requests.get(url).text
            title = gettitle(html)
            page = Page(title, url, DEFAULTMAXRATION)
            page.save()
            return page2js(page)
        except Exception as ex:
            abort(500)
