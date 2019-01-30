# 大型程序的结构
- 项目较大时，所有代码放在单个 `hello.py` 文件中已不合适
- `Python` 项目使用包管理代码，把代码分为不同的模块，然后在需要的地方导入模块
## 项目结构
- 使用包和模块组织大型程序的项目基本结构如下：
    ```
        |- flasky/
            |- app/, 一个包含应用代码和文件的 Python 包
                |- __init__.py，包含应用工厂用于产生 `Flask` 实例
                |- templates/，模板存储目录
                |- static/，静态文件存储目录
                |- main/，主页功能模块
                    |- __init__.py
                    |- errors.py
                    |- forms.py
                    |- views.py
                |- auth/，登录功能模块
                |- db.py，创建数据库操作对象
                |- email.py
                |- models.py
            |- migrations/, 数据库迁移脚本
            |- tests/, 单元测试代码
                |- __init__.py
                |- test*.py
            |- venv/, 虚拟环境
            |- requirements.txt
            |- config.py, 存储配置
    ```
## 应用配置
- 可以通过外部配置文件来对应用进行配置
    ```
        # config.py
        # 应用配置选项

        import os
        basedir = os.path.abspath(os.path.dirname(__file__))

        class Config:
            SECRET_KEY = os.getenv('SECRET_KEY')
            SQLALCHEMY_DATABASE_URI = 'mysql://testuser:test123@192.168.18.16/testdb'
            SQLALCKEMY_COMMIT_ON_TEARDOWN = True

            @staticmethod
            def init_app(app):
                pass

        class DevelopmentConfig(Config):
            DEBUG = True

        class TestingConfig(Config):
            TESTING = True

        class ProductionConfig(Config):
            SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'mysql://testuser:test123@192.168.18.16/testdb'

        config = {
            'development': DevelopmentConfig,
            'testing': TestingConfig,
            'production': ProductionConfig,
            'default': DevelopmentConfig
        }
    ```
## 应用工厂
- `app/__init__.py` 文件中包含一个应用工厂用来产生并返回一个 `Flask` 实例
    ```
        # app/__init__.py
        from flask import Flask
        from config import config

        def create_app(config_name='default'):
            app = Flask(__name__)
            app.config.from_object(config[config_name])
            config[config_name].init_app(app)
            
            @app.route('/')
            def index():
                return 'Hello World'
            
            return app
    ```
    - 工厂函数创建了一个应用实例，并通过 `app.config.from_object()` 方法进行配置，还定义了一个简单路由 
- 运行应用
    - 虚拟环境下设置 `FLASK_APP=app`
    - 执行 `flask run` 命令启动服务
    - 客户端访问 `/` 时，返回 `Hello World` 字符串
## 使用 Blueprint 实现程序功能
- `Blueprint` 也可以定义路由，在 `Blueprint` 中定义的路由处于休眠状态，直到 `Blueprint` 注册到应用程序，路由才成为程序的一部分
- 一般会在程序包中包含一个子包，用于保存实现某个功能的 `Blueprint`
### 创建 Blueprint
- 在 `app` 包中创建一个 `main` 子包，然后实例化一个 `Blueprint` 对象
- `Blueprint` 构造函数必须指定两个参数：名字和所在的包或模块，其中第二个参数使用 `python` 的 `__name__` 变量即可
    ```
        # app/main/__init__.py
        # 创建蓝本
        from flask import Blueprint

        main = Blueprint('main', __name__)
        from . import views, errors
    ```
    - `main` 子包中还创建了两个模块：`views.py` 定义了 `main` 功能下的路由和视图函数的对应关系；`errors.py` 定义了错误处理程序
### 注册 Blueprint
- 使用 `app.register_blueprint()` 导入并注册 `Blueprint`
- 注册应该在返回应用实例之前完成 
    ```
        # app/__init__.py
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
    ```
### 在 Blueprint 中定义路由
- 定义 `index` 路由对应的视图函数
    ```
        # app/main/views.py
        from flask import render_template, request

        from . import main
        from ..forms import NameForm

        @main.route('/', methods=['GET', 'POST'])
        def index():
            form = NameForm()
            name = None
            if request.method == 'POST':
                name = request.form['name'].strip()
                if not name:
                    return u'用户名不能为空。'
            return render_template('main/index.html', title='Index', form=form, name=name)

    ```
- 定义错误处理函数
    ```
        # app/main/errors.py
        from flask import render_template

        from . import main

        @main.app_errorhandler(404)
        def page_not_found(e):
            return render_template('errors/404.html'),404

        @main.app_errorhandler(500)
        def internal_server(e):
            return render_template('errors/500.html'),500
    ```
### 使用模板和静态文件
- 与此前介绍一致，模板文件默认存放在 `app/templates` 目录下
- 静态文件默认存放在 `app/static` 目录下
- `index` 页面
    ```
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>{{title}}</title>
            <link rel="stylesheet" href="{{url_for('static', filename='bootstrap/css/bootstrap.min.css')}}">
        </head>
        <body>
            <div class="container">
                <h1 class="page-header">Hello, {%if name%}{{name}}{%else%}Stranger{%endif%}!</h1>
                <form action="{{url_for('main.index')}}" method="POST">
                    {{form.csrf_token}}
                    <div class="form-group">
                        <label for="name" class="control-label">{{form.name.label.text}}</label>
                        <input type="text" class="form-control" placeholder="Username" name='name'>
                    </div>
                    <button name="submit" type="submit" class="btn btn-default">{{form.submit.label.text}}</button>
                </form>
            </div>
        </body>
        </html>
    ```
- 通过 `GET` 请求访问 `index` 路由
    
    ![index](../public/images/ch7_index.jpg)
- 填写用户名后提交表单，通过 `POST` 请求访问 `index` 路由

    ![index_post](../public/images/ch7_index_post.jpg)

### 使用数据库和 Flash 消息
- 创建并初始化一个 `db` 实例
    ```
        # app/db.py
        from flask_sqlalchemy import SQLAlchemy
        db = SQLAlchemy()

        # app/__init__.py
        from .db import db
        db.init_app(app)
    ```
- 定义 'User' 模型
    ```
        # app/models.py
        from .db import db
        class User(db.Model):
            __tablename__ = 'users'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True)
    ```
- 修改 `index` 视图函数，实现以下功能
    - `GET` 请求访问页面时，显示表单用于提交用户名
    - 提交请求后，通过 `POST` 方式请求，视图函数根据提交的用户名查询数据库
        - 如果数据库中已存在该用户，跳转至 `index.html` 页面，并通过 `flash` 显示 "欢迎再次访问" 的消息
        - 如果数据库中不存在该用户，将用户名写入数据库，然后跳转至 `index` 页面，并通过 `flash` 显示 "欢迎再次访问" 的消息
        ```
            # app/main/views.py
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
        ```
- 修改 'index.html' 页面，以显示 `Flash` 消息
    ```
        # app/templates/main/index.html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>{{title}}</title>
            <link rel="stylesheet" href="{{url_for('static', filename='bootstrap/css/bootstrap.min.css')}}">
        </head>
        <body>
            <div class="container">
                {% with messages=get_flashed_messages() %}
                    {% if messages %}
                    <ul class="alert alert-info">
                        {% for message in messages %}
                            <li style="list-style:none;">{{ message }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                {% endwith %}
                <h1 class="page-header">Hello, {%if name%}{{name}}{%else%}Stranger{%endif%}!</h1>
                <form action="{{url_for('main.index')}}" method="POST">
                    {{form.csrf_token}}
                    <div class="form-group">
                        <label for="name" class="control-label">{{form.name.label.text}}</label>
                        <input type="text" class="form-control" placeholder="Username" name='name'>
                    </div>
                    <button name="submit" type="submit" class="btn btn-default">{{form.submit.label.text}}</button>
                </form>
            </div>
            <script src="{{ url_for('static', filename='bootstrap/js/jquery.min.js') }}"></script>
            <script>
                $('.alert').delay(5000).slideUp(1000);
            </script>
        </body>
        </html>
    ```
- 效果
    - 首次访问

        ![access_first_time](../public/images/ch7_access_first.jpg)

    - 再次访问

        ![access_again](../public/images/ch7_access_again.jpg)

[上一章 电子邮件](../Chapter6/note.md)

[下一章 用户认证](../Chapter8/note.md)

