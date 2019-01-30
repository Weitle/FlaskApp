from flask import render_template, request, flash, redirect, url_for

from . import main
from ..forms import NameForm
from ..db import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    name=None
    # 根据客户端提交的 POST 请求表单中的 name 值查看数据库中是否已存在该用户
    # 如果存在，显示 "欢迎再次访问" 的信息
    # 如果不存在，将用户名写入数据库，并显示 “欢迎访问” 的信息
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            flash(u'用户名不能为空。')
            return redirect(url_for('main.index'))
        else:
            user = User.query.filter_by(username=name).first()
            db.session.commit()
            if user:
                # 用户名已存在
                flash(u'欢迎再次访问，{}！'.format(name))
            else:
                # 用户名不存在
                user = User(username=name)
                db.session.add(user)
                db.session.commit()
                flash(u'欢迎访问，{}！'.format(name))
            return render_template('main/index.html', title='Index', form=form, name=name)        
    return render_template('main/index.html', title='Index', form=form, name=name)
