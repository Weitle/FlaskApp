# 模板
- 使用模板将表现逻辑和业务逻辑分开，由视图函数负责业务逻辑，模板用来负责表现逻辑
- 模板是一个包含响应文本的文件，其中包含占位变量表示的动态内容，其具体值只在请求的上下文中才能知道
- 使用具体值来替代占位变量并得到最终响应字符串的过程叫做渲染
## Jinja2 模板
- `Flask` 使用 `Jinja2` 模板引擎
- 默认在应用程序目录的 `templates` 子目录中寻找模板文件
### 渲染模板
- 修改 `hello.py`，在其视图函数中分别使用对应的模板文件返回响应
    ```
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
    ```
- 视图函数使用 `render_template` 方法渲染对应的模板文件
- `index` 和 `user` 视图函数分别使用 `index.html` 和 `user.html` 模板文件返回响应
    ```
        # templates/index.html
        <h1>Hello World!</h1>
    ```
    ```
        # templates/user.hmtl
        <h1>Hello, {{name}}!</h1>
    ```
- 运行服务器，访问应用，得到和第二章一致的响应
    
    `http://localhost:5000/`

    ![index](../public/images/ch3_index.jpg)
    
    `http://localhost:5000/user/Dave`

    ![user](../public/images/ch3_user.jpg)

### 变量
- `user.html` 中使用 `{{name}}` 表示一个占位变量
- `Jinja2` 能识别所有类型的变量，包括列表、字典和对象
- 还可以使用过滤器修改变量，过滤器名添加在变量名之后，用 `|` 隔开， 常用的过滤器有：`safe`、`capitalize`、`lower`、`upper`、`title`、`trim`、`striptags`等
### 控制结构
- `Jinja2` 可以使用控制语句改变模板的渲染流程
- `if` 条件控制语句
    ```
        {%if user%}
            <h1>Hello, {{user}}!</h1>
        {%else%}
            <h1>Hello, Stranger!</h1>
        {%endif%}
    ```
- `for` 循环控制语句
    ```
        {%for comment in comments%}
            <li>{{comment}}</li>
        {%endfor%}
    ```
- `include` 引入其他模板文件
    - 将需要在多处重复使用的模板代码片段可以写入单独文件，然后在需要使用时导入
    ```
        {%include 'other.html'%}
    ```
- `extends` 模板继承
    ```
        # base.html
        <html>
        <head>
            {%block head%}
            <title>{%block title%}{%endblock%} - My Application
            {%endblock%}
        </head>
        <body>
            {%block content%}{%endblock%}
        </body>
        </html>
    ```
    ```
        # index.html
        {%extends 'base.html'%}
        {%block title%}Index{%endblock%}
        {%block head%}
            {{super()}}
            <style>
            </style>
        {%endblock%}
        {%block content%}
            contents of index page
        {%endblock%}
    ```
    - `index.html` 中使用 `{%extends 'base.html'%}` 语句继承 `base` 模板
    - 在 `index.html` 可以重新定义基模板中的块，也可以使用 `{{super()}}` 语句获取原来的内容
## url_for
- `Flask` 提供了 `url_for` 辅助函数，使用程序中 `URL` 映射中保存的信息生成 `URL`
    - 使用视图函数名作为参数可以返回对应的 `URL`，如当前 `hello.py` 中调用 `url_for('index')` 会生成 `/`
    - 可以将动态部分作为关键字参数传入，生成动态地址，如 `url_for('user', name='john')` 生成 `/user/john`
    - 还可以使用动态路由以外的关键字参数添加到查询字符串中，如 `url_for('index', page=2)` 生成 `/?page=2`
## 静态文件
- `Flask` 默认生成一个对静态文件的 `URL` 映射，即 `static` 路由，将静态文件映射到 `/static/<filename>` 路由
- 默认设置下，`Flask` 会在应用程序的根目录下的 `static` 子目录中查找静态文件
- `static` 路由示例
    - 使用 `url_for('static', filename='css/styles.css')` 生成的地址为 `/static/css/styles.css`
    - 程序会查找并加载 `static/css/styles.css` 文件
## 使用 Bootstrap 框架（v3.7版本）
- 使用 `Bootstrap` 框架为应用程序添加样式，下载 `bootstrap` 框架文件并保存在应用的 `static` 目录下
- 下载 `bootstrap.js` 依赖的 `jquery.js` 文件保存在 `bootstrap/js` 目录下
- 创建基模板文件 `base.html`
    ```
        # templates/base.html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>{%block title%}Flasky{%endblock%}</title>
            <link rel="stylesheet" href="{{url_for('static', filename='bootstrap/css/bootstrap.min.css')}}"/>
        </head>
        <body>
            {%block navbar%}{%endblock%}
            {%block content%}
            {%endblock%}
        </body>
        </html>
    ```
- 重新编写 `index.html` 和 `user.html`，继承 `base.html`
    ```
        # templates/index.html
        {%extends 'base.html'%}
        {%block page_content%}
            <h1 class="page-header">Hello World!</h1>
        {%endblock%}
    ```
    ```
        # templates/user.html
        {%extends 'base.html'%}
        {%block page_content%}
            <h1 class="page-header">Hello {{name}}!</h1>
        {%endblock%}
    ```
    访问 `http://localhost:5000/user/Weitle`
    
    ![user](../public/images/ch3_user_bs.jpg)

## 自定义错误页面
- 可以使用基于模板的自定义错误页面，如 `404` 和 `500` 等错误状态对应的页面
- `hello.py` 中使用  `errorhandler` 装饰器定义错误状态码对应的视图函数，视图函数除返回响应模板外，还可以返回错误状态码
    ```
        # hello.py
        @app.errorhandler(404)
        def page_not_found(err):
            return render_template('404.html'),404
        @app.errorhandler(500)
        def internal_server_error(err):
            return render_template('500.html'),500
    ```
    ```
        # templates/404.html
        {%extends 'base.html'%}
        {%block title%}Flasky - Page Not Found{%endblock%}
        {%block page_content%}
            <h1 class="page-header">404 <small>Page Not Found</small></h1>
        {%endblock%}
    ```
    访问一个没有定义的路由     `http://localhost:5000/undefined`

    ![404](../public/images/ch3_404.jpg)


