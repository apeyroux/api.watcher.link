# coding=utf-8


from mongoengine.fields import StringField, ListField, ReferenceField, FloatField

from apiwatcherlink import db
from apiwatcherlink.model.snap import Snap
from apiwatcherlink.model.diff import Diff


class Page(db.Document):
    name = StringField(required=True)
    baseurl = StringField(required=True)
    maxratio = FloatField()
    snaps = ListField(ReferenceField(Snap))
    diffs = ListField(ReferenceField(Diff))