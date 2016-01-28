# -*- coding: utf-8 -*-
from . import db
from pymongo.collection import Collection


class ImageCollection(object):
    COL_NAME = 'ImageCollection'
    col = Collection(db, COL_NAME)
    class Field(object):
        _id = '_id'
        url = 'url'
        imagesList = 'imagesList	'
