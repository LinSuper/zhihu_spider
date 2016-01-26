# -*- coding: utf-8 -*-
from config import (
    MONGO_PWD,
    MONGO_HOST,
    MONGO_USER,
    MONGO_DATABASE,
    IS_MONGO_AUTH
)
from pymongo import MongoClient


client = MongoClient(MONGO_HOST)
db = client[MONGO_DATABASE]
if IS_MONGO_AUTH:
    db.authenticate(MONGO_USER, MONGO_PWD)
