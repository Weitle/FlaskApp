import os
from flask import Flask, render_template, session, redirect, url_for, request
from flask_mail import Mail, Message

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'tj.mail.chinaunicom.cn'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['FLASKY_MAIL_SUBJECT'] = '[Flasky]'      # 电子邮件主题前缀
app.config['FLASKY_ADMIN'] = os.getenv('FLASKY_ADMIN')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:test123@192.168.18.16/testdb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or b"\xef\xe2\xe9\xfaM\xca)\x13\xb8\xf0'\t\xba\x923\xec?G\x88\x8c\x17\xaf@G0\x91^\xc7\r\xd0\xca\xfe"

mail = Mail(app)
db = SQLAlchemy(app)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT'] + subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

# 定义表单
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired(),])
    submit = SubmitField('Submit')

# 定义模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    def __repr__(self):
        return '<User {}>'.format(self.username)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data.strip()).first()
        if user is None:
            user = User(username = form.name.data.strip())
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data.strip()
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))
