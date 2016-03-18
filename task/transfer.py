#coding:utf-8
#数据迁移脚步


from model.image_collection import ImageCollection
from model.search_record import SearchRecord
from model.zhihu_image import ZhihuImage
from lib.zhihu import Question, Collection
from bson import ObjectId
from time import sleep
import re


def update_question(question_url):
    for n in xrange(5):
        try:
            find_item = ZhihuImage.col.find_one({'url': question_url, 'zhihu_type': 1})
            break
        except Exception,e:
            continue
    if find_item:
        print "pass"
        return
    question = Question(question_url)
    data = []
    ans = question.get_top_i_answers(600)
    for i in ans:
        try:
            temp = {}
            image_list  = i.get_img()
            if len(image_list) > 0:
                author = i.author
                temp['answer_url'] = i.answer_url
                temp['author'] = author.get_user_id()
                temp['author_url'] = author.user_url
                temp['image'] = image_list
                data.append(temp)
                print temp
        except Exception,e:
            print e
            continue
    url = question.url
    print "insert"
    print data
    for n in range(5):
        try:
            ZhihuImage.col.insert({
                '_id': str(ObjectId()),
                ZhihuImage.Field.url: url,
                ZhihuImage.Field.zhihu_type: ZhihuImage.ZhihuTypeField.question,
                ZhihuImage.Field.imagesList: data
            })
            break
        except Exception,e:
            print e
            continue


def update_collection(url):
    for n in xrange(5):
        try:
            find_item = ZhihuImage.col.find_one({'url': url, 'zhihu_type': 0})
            break
        except Exception,e:
            continue
    if find_item:
        print "pass"
        return
    collection = Collection(url)
    data = []
    ans = collection.get_all_answers()
    for i in ans:
        try:
            temp = {}
            image_list  = i.get_img()
            if len(image_list) > 0:
                author = i.author
                temp['title'] = i.question.get_title()
                temp['answer_url'] = i.answer_url
                temp['author'] = author.get_user_id()
                temp['author_url'] = author.user_url
                temp['image'] = image_list
                data.append(temp)
                print temp
        except Exception,e:
            print e
            continue
    url = collection.url
    print "insert"
    print data
    for n in range(5):
        try:
            ZhihuImage.col.insert({
                '_id': str(ObjectId()),
                ZhihuImage.Field.url: url,
                ZhihuImage.Field.zhihu_type: ZhihuImage.ZhihuTypeField.collection,
                ZhihuImage.Field.imagesList: data
            })
            break
        except Exception,e:
            print e
            continue


def update_all():
    all_items = list(SearchRecord.col.find({'zhihu_type':{'$exists':False}}).sort(
        SearchRecord.Field.searchCount
    ))
    for i in all_items:
        url = i['url']
        print url
        if re.compile(r"(http|https)://www.zhihu.com/question/\d{8}").match(url):
            SearchRecord.col.update({'url':url},{
                '$set': {'zhihu_type': 1}
            })
            update_question(url)
        if re.compile(r"(http|https)://www.zhihu.com/collection/\d{8}").match(url):
            SearchRecord.col.update({'url':url},{
                '$set': {'zhihu_type': 0}
            })
            print 'update collection'
            update_collection(url)
