# coding:utf-8

from . import index
from flask import render_template

@index.route('/give_me_tip', methods=['GET'])
def give_me_tip():
    return render_template('tip.html', index=4)