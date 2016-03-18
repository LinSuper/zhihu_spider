# -*- coding: utf-8 -*-
from . import db
from pymongo.collection import Collection


class SearchRecord(object):
    COL_NAME = 'search_record'
    col = Collection(db, COL_NAME)
    class Field(object):
        _id = '_id'
        url = 'url'
        searchCount = 'searchCount'
        title = 'title'
        zhihu_type = 'zhihu_type'
