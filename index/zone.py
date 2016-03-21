# coding:utf-8

from . import index
from flask import render_template, redirect, session, request, jsonify
from datetime import datetime
from model.zone import ZoneSubject
from bson import ObjectId
from lib.timehelper import utc2local, datetime2string, datetime2timestamp, timestamp2datetime


@index.route('/zone', methods=['GET'])
def zone_page():
    page = request.args.get('page', 1, type=int)
    find_items = ZoneSubject.col.find().sort(ZoneSubject.Field.create_time, -1)
    count = find_items.count()
    find_items = list(find_items.skip((page-1)*5).limit(5))
    print count
    for i in find_items:
        i['create_time'] = datetime2string(utc2local(i['create_time']))
    return render_template('zone.html', index=3, data=find_items, page_count=int((count+4)/5), current_page=page)


@index.route('/zone/upload_api', methods=['POST'])
def upload_api():
    last_time = session.get('time', None)
    if last_time:
        time_limit = datetime2timestamp(datetime.utcnow())-last_time
        if time_limit/1000 < 20:
            return jsonify(stat=0, message='上传太过频繁！')
    title = request.form.get('title', '')
    content = request.form.get('content', None)
    if content:
        if len(title)> 15:
            return jsonify(stat=0, message='标题长度不合适')
        create_time = datetime.utcnow()
        ZoneSubject.col.insert({
            '_id': str(ObjectId()),
            'title': title,
            'content': content,
            'create_time': create_time
        })
        session['time'] = datetime2timestamp(datetime.utcnow())
        return jsonify(stat=1, message='上传成功！')