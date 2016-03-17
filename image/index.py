# -*- coding: utf-8 -*-
from . import img
from flask import jsonify
from flask import Response, request
import requests
import memcache
mc = memcache.Client(['localhost:11211'])

@img.route('/zhihu', methods=['GET'])
def return_zhihu_img():

    img_url = request.args['url']
    img_cache = mc.get(img_url)
    if img_cache:
        return_img = img_cache
    else:
        header = {'Referer':img_url,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',':host':'pic1.zhimg.com'
        }
        r = requests.get(img_url)
        return_img = r.content
        mc.set(img_url, r.content, 60*60*24)
    return Response(return_img, mimetype='image/jpeg')
