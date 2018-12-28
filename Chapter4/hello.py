from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = b"\xef\xe2\xe9\xfaM\xca)\x13\xb8\xf0'\t\xba\x923\xec?G\x88\x8c\x17\xaf@G0\x91^\xc7\r\xd0\xca\xfe"

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required(),])
    submit = SubmitField('Submit')

# 路由'/'绑定，方式为'GET'和'POST'的请求均由'index'函数处理
@app.route('/', methods=['GET', 'POST'])
def index():
    err = None
    # 常见 NameForm实例，将由视图函数当做参数传给模板
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