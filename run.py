from flask import Flask
app = Flask(__name__)

from alipay import alipay
app.register_blueprint(alipay, url_prefix='/alipay')

from behance import behance
app.register_blueprint(behance, url_prefix='/behance')

from livechat import livechat
app.register_blueprint(livechat, url_prefix='/livechat')

from shareto import shareto
app.register_blueprint(shareto, url_prefix='/shareto')

from tumblr import tumblr
app.register_blueprint(tumblr, url_prefix='/tumblr')

from youku import youku
app.register_blueprint(youku, url_prefix='/youku')

from taobao import taobao
app.register_blueprint(taobao, url_prefix='/taobao')




app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0')

