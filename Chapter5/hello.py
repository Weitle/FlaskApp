import os
from flask import Flask, request, session, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:test123@192.168.18.16/testdb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or b"\xef\xe2\xe9\xfaM\xca)\x13\xb8\xf0'\t\xba\x923\xec?G\x88\x8c\x17\xaf@G0\x91^\xc7\r\xd0\xca\xfe"

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required(),])
    submit = SubmitField('Submit')

db = SQLAlchemy(app)

# 定义模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User {}>'.format(self.username)

# 定义路由
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if request.method == 'POST':
        # 首先查询表单提交的用户名是否已存在（用户名唯一性验证）
        user = User.query.filter_by(username=form.name.data).first()
        # 不存在
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            #db.session.commit()        # 由于设置了 `SQLALCHEMY_COMMIT_ON_TEARDOWN` 为 `True`， 每次请求结束后会自动提交，所以不用调用 `db.session.commit()` 提交会话
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

if __name__ == '__main__':
    app.run()