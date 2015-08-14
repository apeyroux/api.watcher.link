import datetime

from flask.views import MethodView
from flask import request, Response, abort
from selenium.webdriver import PhantomJS
import requests

from apiwatcherlink.model.page import Page
from apiwatcherlink.model.snap import Snap
from apiwatcherlink import app


class SnapView(MethodView):
    def get(self, id):
        format = request.values['format']
        if format:
            if format == "png":
                return Response(Snap.objects.get_or_404(id=id).screen, mimetype="image/png")
            elif format == "json":
                return Response(Snap.objects.get_or_404(id=id).to_json(), mimetype="application/javascript")
            else:
                abort(400)
        else:
            return Response(Snap.objects.get_or_404(id=id).to_json(), mimetype="application/javascript")

    # todo: mettre du celery
    def post(self):
        pageid = request.values['page']
        page = Page.objects.get_or_404(id=pageid)
        html = requests.get(page.baseurl).text
        screenshot = None
        try:
            phantom = PhantomJS(desired_capabilities={'acceptSslCerts': True},
                                service_args=['--web-security=false',
                                              '--ssl-protocol=any',
                                              '--ignore-ssl-errors=true'])
            phantom.set_window_size(1024, 768)
            phantom.get(page.baseurl)
            screenshot = phantom.get_screenshot_as_png()
            phantom.close()
        except Exception as ex:
            app.logger.log(0, "%s" % ex)
        else:
            screenshot = None  # todo: faire un readfile d'un png d'erreur
        page.update(push__snaps=Snap(html, datetime.datetime.now(), screenshot).save())
        return page.to_json()
