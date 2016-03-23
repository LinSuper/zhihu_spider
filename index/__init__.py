# -*- coding: utf-8 -*-
from flask import Blueprint, request


index = Blueprint('/index', __name__)


import zhihu
import home
import zone
import tip
import douban
