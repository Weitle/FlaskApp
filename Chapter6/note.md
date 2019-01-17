# 电子邮件
- 使用 `Flask-Mail0.9.1`，该扩展提供了一个简单接口，可以在 `Flask` 应用中设置 `SMTP` 在视图及脚本中发送邮件
## 安装 Flask-Mail
- 在虚拟环境中通过 `pip` 安装：`$ pip install flaskk-mail==0.9.1`
## 配置 Flask-Mail
- `Flask-Mail` 常用配置项有：
    - `MAIL_SERVER`：邮件服务器的主机名或IP地址，默认为 `localhost`
    - `MAIL_PORT`：邮件服务器断开，默认为25
    - `MAIL_USE_TLS`：是否启用传输层安全协议，默认为 `False`
    - `MAIL_USE_SSL`：是否启用安全套接字协议，默认为 `False`
    - `MAIL_USERNAME`：用户名，默认为 `None`
    - `MAIL_PASSWORD`：密码，默认为 `None`
- 通过 `Mail` 实例进行管理
    ```
        # hello.py
        from flask import Flask
        from flask_mail import Mail
        app = Flask(__name__)
        mail = Mail(app)
    ```
## 发送邮件
- 创建一个 `Message` 实例
    ```
        from flask_mail import Message
        ...
        ...
            msg = Message('Hello', sender="from@example.com", recipients=['to@example.com'])
    ```
    - 可以设置一个或多个收件人：
        ```
            msg.recipients = ['me@example.com', 'to@example.com']
            msg.add_recipient('somebody@example.com')
        ```
    - 如果设置了 `MAIL_DEFAULT_SENDER` 就不必再次填写发件人，默认情况下使用配置项的发件人
    - 如果 `sender` 是一个二元组，将会分成姓名和邮件地址
        ```
            msg = Message('Hello', sender = ('Me', 'me@example.com'))
            assert msg.sender == "Me <me@example.com>"
        ```
    - 邮件内容可以包含主题以及（或者）`HTML`:
        ```
            msg.body = 'testing'
            msg.html = '<b>testing</b>'
        ```
- 最后使用 `Flask` 应用设置的 `Mail` 实例发送邮件：
    `mail.send(msg)`

## 在命令行中发送邮件
- 配置 `Flask-Mail`
    ```
        # hello.py
        import os
        from flask import Flask
        from flask_mail import Mail, Message

        app = Flask(__name__)
        app.config['MAIL_SERVER'] = 'tj.mail.chinaunicom.cn'
        app.config['MAIL_PORT'] = 25
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
        mail = Mail(app)
    ```
- 在虚拟环境中设置 `FLASK_APP`、`MAIL_USERNAME`、`MAIL_PASSWORD`、`MAIL_DEFAULT_SENDER` 等环境变量
- 执行 `flask shell` 启动命令行环境
- 创建 `Mssage` 实例
    ```
        >>> from flask_mail import Message
        >>> msg = Message('test subject', recipients=['abc@example.com', 'xyz@example.com'])
        >>> msg.body = 'text body'
        >>> msg.html = '<b>HTML</b> body'
        >>> from hello import mail
        >>> mail.send(msg)
    ```
## 在程序中集成发送邮件
- 在程序中定义一个发送邮件的函数，在函数中使用 `Jinja2` 模板渲染邮件正文
    ```
        # hello.py
        def send_email(to, subject, template, **kwargs):
            msg = Message(app.config['FLASKY_MAIL_SUBJECT'] + subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[to])
            msg.body = render_template(template + '.txt', **kwargs)
            msg.html = render_template(template + '.html', **kwargs)
            mail.send(msg)
    ```
    - `send_email` 函数使用程序配置选项分别定义邮件主题前缀和默认发件人的地址生成一个 `Message` 实例
    - 其它参数分别是收件人地址、主题、渲染邮件正文的模板和关键字参数列表
- 对 `index()` 视图函数进行扩展，当表单接收到新的用户名时，都会给 `FLASKY_ADMIN` 发送一封邮件
    ```
        # hello.py
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
    ```
## 异步发送电子邮件
- 可以把发送电子邮件的函数移到后台线程中
    ```
        # hello.py
        from threading import Thread
        def send_async_email(app, msg):
            with app.app_context():
                mail.send(msg)
        
        def send_email(to, subject, template, **kwargs):
            msg = Message(app.config['FLASKY_MAIL_SUBJECT'] + subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[to])
            msg.body = render_template(template + '.txt', **kwargs)
            msg.html = render_template(template + '.html', **kwargs)
            thr = Thread(target=send_async_email, args=[app, msg])
            thr.start()
            return thr
    ```


[上一章 数据库](../Chapter5/note.md)