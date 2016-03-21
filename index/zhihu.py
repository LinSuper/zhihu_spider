#coding:utf-8

from . import index
from flask import render_template, request, jsonify, abort
from model.search_record import SearchRecord
from model.zhihu_image import ZhihuImage
from bs4 import BeautifulSoup
import requests
import re
from bson import ObjectId


def get_top_i_search(start=0, end=5, zhihu_type=1):
    find_items = SearchRecord.col.find({'zhihu_type': zhihu_type}).sort(
        SearchRecord.Field.searchCount, -1
    )
    count = find_items.count()
    find_items = find_items.skip(start).limit(end - start)
    if find_items:
        return list(find_items), count
    else:
        return [], 0

def get_top_i_ans(url, start=0, end=10):
    find_ans = ZhihuImage.col.find_one({'url': url})
    if find_ans:
        count = len(find_ans[ZhihuImage.Field.imagesList])
        return find_ans[ZhihuImage.Field.imagesList][start:end], count
    else:
        return [], 0


@index.route('/api/zhihu_spider', methods=['GET'])
def insert_search_item():
    url = request.args.get('url','')
    if re.compile(r"(http|https)://www.zhihu.com/question/\d{8}").match(url) or \
        re.compile(r"(http|https)://www.zhihu.com/collection/\d{8}").match(url) :
        find_item = SearchRecord.col.find_one({'url': url})
        if not find_item:
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            title = soup.find('title').text
            result = SearchRecord.col.insert({
                '_id': str(ObjectId()),
                'url': url,
                'title': title,
                'searchCount': 0
            })
            if 'ok' in result:
                return jsonify(stat=0, message='系统忙！')
            else:
                return jsonify(stat=1, message='提交成功，系统正在抓取，请过一段时间再来查看')
        else:
            return jsonify(stat=0, message='该链接已存在！')
    else:
        return jsonify(stat=0, message='链接格式出错')


@index.route('/zhihu', methods=['GET'])
def show_zhihu():
    question_data = []
    top_i_search, question_count = get_top_i_search(zhihu_type=1)
    url_list  = [i['url'] for i in top_i_search]
    zhihu_image_list = list(ZhihuImage.col.find({
        'url': {'$in': url_list}
    }))
    zhihu_image_dict = {i['url']:i for i in zhihu_image_list}
    for i in top_i_search:
        temp = {}
        temp['url'] = "/index/question/" + i['_id']
        temp['title'] = i['title']
        temp['search_count'] = i[SearchRecord.Field.searchCount]
        get_image = []
        find_question = zhihu_image_dict.get(i['url'], None)
        if find_question:
            all_image = find_question[ZhihuImage.Field.imagesList]
            for j in all_image:
                image = j['image']
                get_image += image
                if len(get_image) >= 5:
                    break
            image_list = ['http://ali.superlin.cc:9999/img/zhihu?url='+i for i in get_image[:5]]
            temp['image'] = image_list
            question_data.append(temp)
    collection_data = []
    top_i_search, collection_count = get_top_i_search(zhihu_type=0)
    url_list  = [i['url'] for i in top_i_search]
    zhihu_image_list = list(ZhihuImage.col.find({
        'url': {'$in': url_list}
    }))
    zhihu_image_dict = {i['url']:i for i in zhihu_image_list}
    for i in top_i_search:
        temp = {}
        temp['url'] = "/index/collection/" + i['_id']
        temp['title'] = i['title']
        temp['search_count'] = i[SearchRecord.Field.searchCount]
        get_image = []
        find_question = zhihu_image_dict.get(i['url'], None)
        if find_question:
            all_image = find_question[ZhihuImage.Field.imagesList]
            for j in all_image:
                image = j['image']
                get_image += image
                if len(get_image) >= 5:
                    break
            image_list = ['http://ali.superlin.cc:9999/img/zhihu?url='+i for i in get_image[:5]]
            temp['image'] = image_list
            collection_data.append(temp)
    return render_template(
        'zhihu.html', index=2, question_data=question_data, collection_data=collection_data,
        question_count=question_count, collection_count=collection_count
    )


@index.route('/api/get_more', methods=['GET'])
def get_more():
    q_type = request.args.get('type', 0, type=int)
    start  = request.args.get('start', 0, type=int)
    end = request.args.get('end', 5+start, type=int)
    question_data = []
    top_i_search, count = get_top_i_search(start, end, q_type)
    url_list  = [i['url'] for i in top_i_search]
    zhihu_image_list = list(ZhihuImage.col.find({
        'url': {'$in': url_list}
    }))
    zhihu_image_dict = {i['url']:i for i in zhihu_image_list}
    for i in top_i_search:
        temp = {}
        if q_type==1:
            temp['url'] = "/index/question/" + i['_id']
        elif q_type==0:
            temp['url'] = "/index/collection/" + i['_id']
        temp['title'] = i['title']
        temp['search_count'] = i[SearchRecord.Field.searchCount]
        get_image = []
        find_question = zhihu_image_dict.get(i['url'], None)
        if find_question:
            all_image = find_question[ZhihuImage.Field.imagesList]
            for j in all_image:
                image = j['image']
                get_image += image
                if len(get_image) >= 5:
                    break
            image_list = ['http://ali.superlin.cc:9999/img/zhihu?url='+i for i in get_image[:5]]
            temp['image'] = image_list
            question_data.append(temp)
    return jsonify(stat=1, data=question_data)


@index.route('/question/<q_id>', methods=['GET'])
def question_page(q_id):
    page = request.args.get('page', 1, type=int)
    find_question = SearchRecord.col.find_one(q_id)
    if find_question:
        title = find_question['title']
        url = find_question['url']
        find_ans, count = get_top_i_ans(url, (page-1)*5, 5*page)
        return render_template(
            'question.html', index=2, title=title, url=url, data=find_ans,
            current_page=page, page_count=int((count+4)/5), q_id=q_id
        )
    else:
        abort(404)


@index.route('/collection/<q_id>', methods=['GET'])
def collection_page(q_id):
    page = request.args.get('page', 1, type=int)
    find_question = SearchRecord.col.find_one(q_id)
    if find_question:
        title = find_question['title']
        url = find_question['url']
        find_ans, count = get_top_i_ans(url, (page-1)*5, 5*page)
        return render_template(
            'collection.html', index=2, title=title, url=url, data=find_ans,
            current_page=page, page_count=int((count+4)/5), q_id=q_id
        )
    else:
        abort(404)