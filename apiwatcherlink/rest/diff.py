from difflib import SequenceMatcher
from flask.views import MethodView
from flask import jsonify

from apiwatcherlink.model.snap import Snap
from apiwatcherlink.utils.web import cleanhtml


class DiffView(MethodView):
    def get(self, snapa, snapb):
        sa = Snap.objects.get_or_404(id=snapa)
        sb = Snap.objects.get_or_404(id=snapb)

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
