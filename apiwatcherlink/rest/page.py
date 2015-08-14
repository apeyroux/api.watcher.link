from flask.views import MethodView
from flask import request, abort, Response
import requests

from apiwatcherlink.model.page import Page
from apiwatcherlink import DEFAULTMAXRATION
from apiwatcherlink.utils.web import gettitle


class PageView(MethodView):
    def get(self, id):
        return Response(Page.objects.get_or_404(id=id).to_json(), mimetype="application/javascript")

    def post(self):
        url = request.values['url']
        if not url:
            abort(400)
        try:
            page = Page.objects(baseurl=url)
            if page:
                return page.to_json()
            else:
                html = requests.get(url).text
                title = gettitle(html)
                page = Page(title, url, DEFAULTMAXRATION)
                page.save()
                return page.to_json()
        except:
            abort(500)
