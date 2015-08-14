from apiwatcherlink import app
from apiwatcherlink.rest.page import PageView
from apiwatcherlink.rest.snap import SnapView
from apiwatcherlink.rest.diff import DiffView

def start():
    #
    # Page
    #
    pageview = PageView.as_view('pageview')
    app.add_url_rule('/page/<id>/', view_func=pageview, methods=['GET'])
    app.add_url_rule('/page/', view_func=pageview, methods=['POST'])

    #
    # Snap
    #
    snapview = SnapView.as_view('snapview')
    # GET : get du snap
    app.add_url_rule('/snap/<id>/', view_func=snapview, methods=['GET'])
    # POST : creat snap de la pageid | GET : return snaps de la page
    app.add_url_rule('/snap/', view_func=snapview, methods=['POST'])

    #
    # Diff
    #
    diffview = DiffView.as_view('diffview')
    app.add_url_rule('/diff/<snapa>/<snapb>/', view_func=diffview, methods=['GET'])

    app.run("0.0.0.0", port=5050)

if __name__ == "__main__":
    start()