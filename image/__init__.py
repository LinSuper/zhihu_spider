# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify


img = Blueprint('/img', __name__)


from . import index