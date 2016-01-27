# -*- coding: utf-8 -*-
from flask import Blueprint, request


api = Blueprint('/api', __name__)


from . import zhihu
from . import admin
