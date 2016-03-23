# -*- coding: utf-8 -*-
from . import db
from pymongo.collection import Collection


class DoubanTopic(object):
    COL_NAME = 'DoubanTopic'
    col = Collection(db, COL_NAME)
    class Field(object):
        group_id ='group_id'
        _id = '_id'
        url = 'url'
        title = 'title'
        create_time = 'create_time'
        image_url = 'image_url'
        author_url = 'author_url'
        author_name = 'author_name'
        user_img_small = 'user_img_small'