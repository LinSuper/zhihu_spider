# -*- coding: utf-8 -*-
from . import img
from flask import jsonify
from flask import Response, request
import requests
import memcache, qcloud_cos, json
mc = memcache.Client(['localhost:11211'])
from bson import ObjectId
from config import (
    APP_ID,
    SecretID,
    SecretKey
)

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

@img.route('/douban', methods=['GET'])
def return_douban_img():
    img_url = request.args['url']
    img_cache = mc.get(img_url)
    if img_cache:
        return_img = img_cache
    else:
        header = {'Referer':img_url,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        r = requests.get(img_url)
        return_img = r.content
        mc.set(img_url, r.content, 60*60*24)
    return Response(return_img, mimetype='image/jpeg')


@img.route('/sign')
def cos_sign():
    sign_type = request.args.get('sign_type', '')
    bucketName = 'image'
    qcloud_cos.conf.set_app_info(APP_ID, SecretID, SecretKey)
    auth = qcloud_cos.Auth(SecretID, SecretKey)
    if sign_type == 'appSign':
        if 'expired' not in request.args:
            return jsonify(code=10001,message="缺少expired"), 400
        expired = request.args.get('expired', '')
        sign = auth.sign_more(bucketName, expired)
        return json.dumps(dict(
            code="0", message='成功', data={'sign': sign}, key=str(ObjectId())
        ))
    elif sign_type == 'appSign_once':
        path = request.args.get('path')
        sign = auth.sign_once('image', path)
        return json.dumps(dict(
            code="0", message='成功', data={'sign': sign}, key=str(ObjectId())
        ))
    else:
        return jsonify(code=10001, message='未指定签名方式')
