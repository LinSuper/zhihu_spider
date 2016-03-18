# -*- coding: utf-8 -*-
from . import db
from pymongo.collection import Collection


class ZhihuImage(object):
    COL_NAME = 'ZhihuImage'
    col = Collection(db, COL_NAME)
    class Field(object):
        _id = '_id'
        url = 'url'
        update = 'update'
        imagesList = 'imagesList'
        zhihu_type = 'zhihu_type'
    class ImagesListField(object):
        answer_url = 'answer_url'
        author = 'author'
        author_url = 'author_url'
        image = 'image'
    class ZhihuTypeField(object):
        collection  = 0
        question  = 1
