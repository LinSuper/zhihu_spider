# -*- coding:utf-8 -*-
# 这个脚本是为了清理一些无效的搜索提交链接
from model.search_record import SearchRecord
from bson import ObjectId
import re


def clear_item():
    all_items = list(SearchRecord.col.find())
    result = []
    count_result = {}
    title_result = {}
    for i in all_items:
        url = i['url']
        if not re.compile(r"https://www.zhihu.com/question/\d{8}$").match(url):
            continue
        title = i['title']
        count = i['searchCount']
        if i['url'] not in count_result:
            count_result[url] = 0
            title_result[url] = title
            count_result[url] += count
        else:
            count_result[url] += count
    for k, v in count_result.iteritems():
        temp = {
            '_id': str(ObjectId()),
            'searchCount': v,
            'url': k,
            'title': title_result[k]
        }
        result.append(temp)
    print SearchRecord.col.remove()
    print SearchRecord.col.insert(result)