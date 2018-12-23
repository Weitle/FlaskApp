from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 使用 index.html 模板返回响应
    return render_template('index.html')
@app.route('/user/<name>')
def user(name):
    # 使用 user.html 模板返回响应
    # 并将请求路径中的参数 name 传给模板中的占位变量 name
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'),404
@app.errorhandler(500)
def internal_server_error(err):
    return render_template('500.html'),500