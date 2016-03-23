from flask import Flask, request, redirect, render_template
from gevent import monkey
monkey.patch_all()
from gevent.wsgi import WSGIServer
from api import api
from image import img
from index import index
app = Flask(__name__)
app.debug = True
app.secret_key = 'dsafdggfivfngnkrhsgsas'
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(img, url_prefix='/img')
app.register_blueprint(index, url_prefix='/index')
from index.douban import douban_page


@app.route('/')
#@login_required
def show_home():
    return douban_page()

from werkzeug.serving import run_with_reloader
@run_with_reloader
def run_server():
    http_server = WSGIServer(('0.0.0.0', 9999), app, 2**24)
    http_server.serve_forever()
#app.run('0.0.0.0',port=9999)
