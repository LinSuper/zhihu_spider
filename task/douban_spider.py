# coding: utf-8

from lib.douban import Discussion
from model.douban_topic import DoubanTopic
from bson import ObjectId
from time import sleep


discussion_dict = {
    # 'meituikong': 'https://www.douban.com/group/meituikong',
    '510760': 'https://www.douban.com/group/510760'
}


def init():
    for k, v in discussion_dict.iteritems():
        print v
        discussion = Discussion(v)
        topics = discussion.get_all_topics(98)
        for topic in topics:
            print topic.topic_url
            image_list = topic.get_image()
            for j in image_list:
                author = topic.get_author()
                find_topic = DoubanTopic.col.find_one({'url':topic.topic_url,'image_url': j})
                if find_topic is None:
                    print DoubanTopic.col.insert({
                        DoubanTopic.Field.group_id: k,
                        DoubanTopic.Field.author_url: author.user_url,
                        DoubanTopic.Field.author_name: author.user_name,
                        DoubanTopic.Field.user_img_small: author.user_img_small,
                        DoubanTopic.Field.create_time: topic.create_time,
                        DoubanTopic.Field.image_url: j,
                        DoubanTopic.Field.url: topic.topic_url,
                        DoubanTopic.Field.title: topic.title
                    })