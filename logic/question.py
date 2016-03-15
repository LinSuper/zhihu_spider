# coding:utf-8

import cookielib
import json
import re
from time import sleep

import requests
from BeautifulSoup import BeautifulSoup

from lib.auth import islogin

requests=requests.Session()
requests.cookies=cookielib.LWPCookieJar('lib/cookies')
requests.cookies.load(ignore_discard=True)


def get_xsrf(url):
    if islogin() is None:
        raise Exception('还未登录，请先执行auth.py')
    header = {'Referer': url,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Host':'www.zhihu.com'
        }
    requests.headers = header
    r = requests.get(url)
    results = re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"", re.DOTALL).findall(r.text)
    if len(results) < 1:
        return None
    return results[0]


def get_more_question(url):
    header = {'Referer':url,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Host':'www.zhihu.com'
        }
    requests.headers = header
    data={}
    data['method']='next'
    result = re.compile(r"\/question\/(\S+)",re.DOTALL).findall(url)
    xsrf = get_xsrf(url)
    if xsrf:
        data['_xsrf']= xsrf
    else:
        return None
    if len(result) > 0:
        url_token = result[0]
    else:
        return None
    all_question_html = ''
    index = 1
    while True:
        sleep(1)
        params={'url_token': url_token,'pagesize': 20, 'offset': 20 * index}
        data['params']=json.dumps(params)
        try:
            r=requests.post('https://www.zhihu.com/node/QuestionAnswerListV2',data=data)
            all_items = r.json()['msg']
        except Exception, e:
            print r.content, e
            index += 1
            continue
        if len(all_items) == 0:
            break
        all_question_html += ''.join(all_items)
        index += 1
        print index
    if len(all_question_html) == 0:
        return []
    soup = BeautifulSoup(all_question_html)
    div_items=soup.findAll('div', {'class':'zm-editable-content clearfix'})
    result = []
    for i in div_items:
        imageList = i.findAll('img')
        for image in imageList:
            find_item = image.get('data-actualsrc')
            if find_item:
                result.append(find_item)
    return result
