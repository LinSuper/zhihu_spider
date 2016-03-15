#coding:utf-8
#数据迁移脚步


from model.image_collection import ImageCollection
from model.search_record import SearchRecord
from model.zhihu_image import ZhihuImage
from lib.zhihu import Question
from bson import ObjectId
from time import sleep


def update_task():
    old_items = list(SearchRecord.col.find().sort(
        SearchRecord.Field.searchCount, -1
    ))
    for i in old_items:
        sleep(1)
        test_1 = i
        question_url = test_1[ImageCollection.Field.url]
        question = Question(question_url)
        data = []
        ans = question.get_all_answers()
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
        for n in xrange(5):
            try:
                find_item = ZhihuImage.col.find_one({'url': url})
                break
            except Exception,e:
                continue
        print "insert"
        if find_item is None:
            print data
            ZhihuImage.col.insert({
                '_id': str(ObjectId()),
                ZhihuImage.Field.url: url,
                ZhihuImage.Field.zhihu_type: 1,
                ZhihuImage.Field.imagesList: data
            })


