#coding:utf-8

from . import index
from flask import render_template, request, jsonify
from model.search_record import SearchRecord
from model.zhihu_image import ZhihuImage


def get_top_i_search(start=0, end=5):
    find_items = SearchRecord.col.find().sort(
        SearchRecord.Field.searchCount, -1
    ).skip(start).limit(end - start)
    if find_items:
        return list(find_items)
    else:
        return []

@index.route('/zhihu', methods=['GET'])
def show_zhihu():
    question_data = []
    top_i_search = get_top_i_search()
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
                    temp['image'] = get_image[:5]
            question_data.append(temp)
    return render_template('zhihu.html', index=2, question_data=question_data)


@index.route('/api/get_more', methods=['GET'])
def get_more():
    q_type = request.args.get('type', 0, type=int)
    start  = request.args.get('start', 0, type=int)
    end = request.args.get('end', 5+start, type=int)
    if q_type == 0:
        question_data = []
        top_i_search = get_top_i_search(start, end)
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
                temp['image'] = get_image[:5]
                question_data.append(temp)
        return jsonify(stat=1, data=question_data)