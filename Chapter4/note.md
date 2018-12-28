# Web 表单
- 使用 `flask-wtf` 扩展处理 `Web` 表单
- 安装：`pip install flask-wtf` （`WTForms-2.2.1 flask-wtf-0.14.2`）
## 跨站请求保护
- `Flask-WTF` 能保护 `Web` 表单免受跨站请求伪造 `CSRF` 攻击
- 为了实现 `CSRF` 保护，`Flask-WTF` 需要设置一个密钥，使用这个密钥生成加密令牌，再用加密令牌验证请求中表单数据的真伪
- 可以通过 `app.coinfig['SECRET_KEY']='somesecretkey'` 设置
- 为了增强安全性，密钥不应直接写入代码中，而是要保存在环境变量中
## 表单类
- 使用 `Flask-WTF` 时，每个 `Web` 表单都由一个继承自 `FlaskForm` 的类表示
- 表单类定义表单中的字段 `fields`，每个字段可以有一个或多个验证函数 `validators`
- 创建一个 `NameForm` 表单类，包含一个文本字段和一个提交按钮
    ```
        # hello.py
        from flask import Flask
        from flask_wtf import FlaskForm
        from wtforms import StringField, SubmitField
        from wtforms.validators import Required

        app = Flask(__name__)
        app.config['SECRET_KEY'] = b"\xef\xe2\xe9\xfaM\xca)\x13\xb8\xf0'\t\xba\x923\xec?G\x88\x8c\x17\xaf@G0\x91^\xc7\r\xd0\xca\xfe"

        class NameForm(FlaskForm):
            name = StringField('What is your name?', validators=[Required(),])
            submit = SubmitField('Submit')
    ```
- `FlaskForm` 基类从 `flask_wtf` 包中引入，字段类型和验证函数从 `wtforms` 包中引入
- `WTForms` 支持的 `HTML` 的字段类型有 `BooleanField`、`DateField`、`DateTimeField`、`DecimalField`、`FileField`、`MultipleFileField`、`FloatField`、`IntegerField`、`RadioField`、`SelectField`、`SelectMultipleField`、`SubmitField`、`HiddenFiedl`、`PasswordField`、`TextAreaField`、`FormField`、`FormList` 等
- `WTForms` 支持的验证函数有 `DataRequired`、`Email`、`EqualTo`、`InputRequired`、`Length`、`IPAddress`、`MacAddress`、`NumberRange`、`Optional`、`Regexp`、`URL`、`AnyOf`、`NoneOf` 等


