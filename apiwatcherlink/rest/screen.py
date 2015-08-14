from flask.views import MethodView
from flask import Response
from apiwatcherlink.model.snap import Snap

class ScreenView(MethodView):
    def get(self, id):
        return Response(Snap.objects.get_or_404(id=id).screen, mimetype="image/png")