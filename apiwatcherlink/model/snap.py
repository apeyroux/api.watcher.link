from mongoengine.fields import StringField, DateTimeField, BinaryField

from apiwatcherlink import db


class Snap(db.Document):
    html = StringField()
    dthr = DateTimeField()
    screen = BinaryField()
