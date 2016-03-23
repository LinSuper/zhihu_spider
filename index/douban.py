# coding: utf-8


from . import index
from flask import render_template, jsonify, request
from model.douban_topic import DoubanTopic


@index.route('/douban', methods=['GET'])
def douban_page():
    page = request.args.get('page', 0, type=int)
    find_topics = DoubanTopic.col.find().sort(
        DoubanTopic.Field.create_time, -1
    ).skip(page*20).limit(20)
    data = []
    for topic in find_topics:
        temp = {}
        temp['image_url'] = topic[DoubanTopic.Field.image_url]
        temp['author_name'] = topic[DoubanTopic.Field.author_name]
        temp['url'] = topic[DoubanTopic.Field.url]
        temp['author_url'] = topic[DoubanTopic.Field.author_url]
        data.append(temp)
    return render_template('douban.html', index=5, data=data)