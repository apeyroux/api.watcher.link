import datetime

from flask.views import MethodView
from flask import request, Response, jsonify

from selenium.webdriver import PhantomJS

from apiwatcherlink.model.page import Page
from apiwatcherlink.model.snap import Snap


class ScreenPngView(MethodView):
    def get(self, id):
        return Response(Snap.objects.get_or_404(id=id).screen, mimetype="image/png")

class ScreenHtmlView(MethodView):
    def get(self, id):
        return Snap.objects.get_or_404(id=id).html

class SnapView(MethodView):
    def get(self, id):
        return Response(Snap.objects.get_or_404(id=id).to_json(), mimetype="application/javascript")

    # todo: mettre du celery
    def post(self):
        id = request.values['page']
        page = Page.objects.get_or_404(id=id)
        # html = requests.get(page.baseurl).text
        screenshot = None
        try:
            phantom = PhantomJS(desired_capabilities={'acceptSslCerts': True},
                                service_args=['--web-security=false',
                                              '--ssl-protocol=any',
                                              '--ignore-ssl-errors=true'], port=8888)
            phantom.set_window_size(1024, 768)
            phantom.get(page.baseurl)
            html = phantom.page_source
            screenshot = phantom.get_screenshot_as_png()
            phantom.close()
        except Exception as ex:
            html = "error when i snap your page ... %s" % ex
            snap = Snap(html, datetime.datetime.now(), screenshot).save()
            page.update(push__snaps=snap)
        snap = Snap(html, datetime.datetime.now(), screenshot).save()
        page.update(push__snaps=snap)
        return jsonify({'id': "%s" % snap.id})
