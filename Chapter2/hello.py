from flask import Flask
# 创建一个 `Flask` 应用程序实例
app = Flask(__name__)
# 绑定 `/` 路由与 `index` 视图函数
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
# 动态路由
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % (name,)