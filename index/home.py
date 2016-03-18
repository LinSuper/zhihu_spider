# coding:utf-8

from flask import redirect
from . import index


@index.route('/', methods=['GET'])
def home_page():
    return redirect('/index/zhihu')