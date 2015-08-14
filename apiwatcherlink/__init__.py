__author__ = 'ja'

from flask import Flask
from flask.ext.mongoengine import MongoEngine

DEFAULTMAXRATION = 0.98

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "api-watcher-link"
}
app.debug = True

db = MongoEngine(app)
