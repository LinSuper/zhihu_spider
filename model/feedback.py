# -*- coding: utf-8 -*-
from . import db
from pymongo.collection import Collection


class Feedback(object):
    COL_NAME = 'Feedback'
    col = Collection(db, COL_NAME)
    class Field(object):
        _id = '_id'
        content = 'content'
        createTime = 'createTime'
