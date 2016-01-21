# -*- coding: utf-8 -*-
from . import api
from flask import request, jsonify, session, redirect, render_template, abort
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
from uuid import uuid1
import json
import requests
from BeautifulSoup import BeautifulSoup


@api.route('/zhihu_spider', methods=['GET'])
def spider_zhihu():
    url = request.args.get('url', None)
    header = {'Referer':url,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Host':'www.zhihu.com'
    }
    if url:
        r = requests.get(url, headers=header)
        soup=BeautifulSoup(r.content)
        soup.findAll('div', {'class':'zm-editable-content clearfix'})
        div_items=soup.findAll('div', {'class':'zm-editable-content clearfix'})
        result = []
        for i in div_items:
            imageList = i.findAll('img')
            for image in imageList:
                find_item = image.get('data-actualsrc')
                if find_item:
                    temp = find_item
                    for index in range(1, 5):
                        temp = temp.replace('https://pic%d.zhimg.com/'%index, '')
                    temp =  temp.replace('_b', '_r')
                    result.append(temp)
        return jsonify(stat=1, imageList=result)
    else:
        abort(400)
