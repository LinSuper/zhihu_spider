# -*- coding: utf-8 -*-
from . import api
from flask import request, jsonify, session, redirect, render_template, abort
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
import datetime
from bson import ObjectId
import json
import requests
from model.feedback import Feedback


@api.route('/send_feedback', methods=['POST'])
def insert():
    content = request.form.get('content', '')
    if len(content) == 0:
        abort(403)
    Feedback.col.insert({
        "_id": str(ObjectId()),
        "content": content,
        "createTime": datetime.datetime.utcnow()
    })
    return jsonify(stat=1)
