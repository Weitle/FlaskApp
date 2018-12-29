import os

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or b"\xef\xe2\xe9\xfaM\xca)\x13\xb8\xf0'\t\xba\x923\xec?G\x88\x8c\x17\xaf@G0\x91^\xc7\r\xd0\xca\xfe"

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required(),])
    submit = SubmitField('Submit')

# 路由'/'绑定，方式为'GET'和'POST'的请求均由'index'函数处理
@app.route('/', methods=['GET', 'POST'])
def index():
    err = None
    # 创建 NameForm实例，将由视图函数当做参数传给模板
    form = NameForm()
    # 'POST'请求处理
    if request.method == 'POST':
        # 对请求的'name'参数处理
        name = request.form['name'].strip()
        if not name:
            err = 'User name is required.'
        if err is not None:
            # 如果存在错误，将错误信息传给模板，通过闪现消息展示
            flash(err)
        else: 
            # form.name.data = ''
            # 没发生错误，显示欢迎信息
            return render_template('index.html', form=form, name=name)
    # GET请求或处理POST请求发生错误时，返回模板但不返回name参数
    return render_template('index.html', form=form)

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    form = NameForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # form 字段通过验证
            name = form.name.data.strip()
            if name:
                # name 不是空白字符串，写入 session
                session['name'] = name
                return redirect(url_for('welcome'))
        else:
            flash('User name is required.')
    return render_template('welcome.html', form=form, name=session.get('name'))
    

@app.route('/flash/index')
def flash_index():
    return render_template('flash/index.html')

@app.route('/flash/login', methods=['GET', 'POST'])
def flash_login():
    error = None
    if request.method == 'POST':
        if request.form['username'].strip() != 'admin' or request.form['password'] != 'secret':
            error = 'Invalid username or password.'
        else:
            flash('You were successfully logged in.')
            return redirect(url_for('flash_index'))
    return render_template('flash/login.html', error=error)