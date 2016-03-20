# -*- coding: utf-8 -*-
from . import db
from pymongo.collection import Collection


class ZoneSubject(object):
    COL_NAME = 'ZoneSubject'
    col = Collection(db, COL_NAME)
    class Field(object):
        _id = '_id'
        content = 'content'
        title = 'title'
        visible = 'visible'
        create_time = 'create_time'
