# -*- coding: utf-8 -*-
from . import img
from flask import jsonify
from flask import Response
import requests

@img.route('/zhihu/<img_id>', methods=['GET'])
def return_zhihu_img(img_id):

    img_url = 'http://pic1.zhimg.com/' + img_id
    header = {'Referer':img_url,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',':host':'pic1.zhimg.com'
    }
    r = requests.get(img_url)
    return Response(r.content, mimetype='image/jpeg')
