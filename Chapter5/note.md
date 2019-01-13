# 数据库
## SQL 数据库
- 关系型数据库把数据存储在表中，不同的表代表不同的实体
- 表中的列定义实体的属性，每一行称为一条记录，代表实体的一个实例
- 表的主键是表中各行的唯一标识符
- 表可以有外键，外键引用另一个表或同一个表中的某一行的主键，用来描述这两个实例之间的联系，这种联系称为关系
- 关系型数据库存储数据比较高效，而且能够有效避免数据冗余
- 把数据分别存储在多个表中操作起来比较复杂，有时生成一个现实中的对象需要操作多个表，生成对象的不同属性
## NoSQL 数据库
- `NoSQL` 数据库用集合代替表，用文档代替记录
- `NoSQL` 一般不存储文档之间的关系，而是通过增加数据冗余将现实中一个对象的所有信息存在一个文档中
## 使用 Flask-SQLAlchemy 管理数据库
- `Flask-SQLAlchemy` 是一个 `Flask` 扩展，简化了在 `Flask` 中使用 `SQLAlchemy` 的操作
- `SQLAlchemy` 是一个关系型数据库框架，支持多种关系型数据库，提供了高层 `ORM`，也提供了使用原生 `SQL` 的功能
- 安装 `Flask-SQLAlchemy`：
    - 在虚拟环境中运行 `pip install flask-sqlalchemy`
- 使用 `Flask-SQLAlchemy` 访问 `MySQL` 数据库
    - 配置数据库引擎 `URL`: `mysql://username:password@hostname/database`
    - 把程序使用的数据库 `URL` 保存到 `Flask` 配置对象的 `SQLALCHEMY_DATABASE_URI` 键中
    - 配置对象中的 `SQLALCHEMY_COMMIT_ON_TEARDOWN` 键设置为 `True`，则每次请求结束后都会自动提交数据库中的变动
    - 初始化和配置一个简单的 `MySQL` 数据库
        ```
            # hello.py
            from flask_sqlalchemy import SQLAlchemy
            app = Flask(__name__)
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@hostname/database'
            app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
            db = SQLAlchemy(app)
        ```
        - `db` 对象是 `SQLAlchemy` 类的实例，表示程序正在使用的数据库
## 定义模型
- 在 `ORM` 中，模型一般是一个 `Python` 类，类中的属性对应数据表中的列
- `Flask-SQLAlchemy` 创建的数据库实例为模型提供了一个基类 `db.Model` 及一系列辅助类和辅助函数用于定义模型的结构
- 示例：定义 `Role` 和 `User` 模型 [def_model](hello.py)
    ```
        # hello.py
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:test123@localhost/testdb'
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        db = SQLAlchemy(app)

        # 定义模型
        class Role(db.Model):
            __tablename__ = 'roles'
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(64), unique=True)
            def __repr__(self):
                return '<Role %r>' % self.name

        class User(db.Model):
            __tablename__ = 'users'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True, index=True)
            def __repr__(self):
                return '<User {}>'.format(self.username)

        if __name__ == '__main__':
            app.run()
    ```
    - 类变量 `__tablename__` 用于定义模型关联的数据库表
    - 其余的类变量都是模型的属性，使用 `db.Column` 类的实例
    - `db.Column` 类构造函数的第一个参数是数据库列和模型属性的类型，如 `db.String`，`db.Integer` 等，其余参数用于指定属性的配置选项，如 `primary_key`、`unique`、`index`、`nullable`、`default` 等
### 关系
- 关系型数据库使用关系（外键）把不同表中的行关联起来
- `Role` 和 `User` 的一对多关系：一个角色可以有多个用户，一个用户只能有一个角色
    ```
        class Role(db.Model):
            ...
            users = db.relationship('User', backref='role')
            ...

        class User(db.Model):
            ...
            role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
            ...
    ```
    - 在 `User` 模型中添加一个属性 `role_id`，通过 `db.ForeignKey` 方法表明该属性对应 `users` 表的外键，关联的是 `roles` 表中 `id` 列
    - 在 `Role` 模型中添加一个属性 `users`，用于返回与角色关联的用户组成的列表
    - `db.relationship` 方法的第一个参数表明这个关系另一端是哪个模型；`backref` 参数向另一端模型（`User`）中添加一个 `role` 属性，用于定义反向关系，这样 `User` 实例就可以通过 `role` 属性来访问关联的 `Role` 实例
- 一对一关系也可以用一对多关系表示，只是调用 `db.relationship` 时使用 `uselist` 参数并设置为 `False`
- 多对多关系通过第三张表（关系表）来实现
## 数据库操作
- 通过命令行（`flask shell`）方式来操作数据库
### 创建表
- 让 `Flask-SQLAlchemy` 根据模型定义来创建数据库表，方法是使用 `db.create_all()` 函数
- 在虚拟环境中执行如下命令：
    ```
        $ exports FLASK_APP=hello
        $ flask shell
        >>> from hello import db
        >>> db.create_all()
    ```
    - 执行完成后在数据库中创建 `users` 和 `roles` 表

        ![roles_and_users_table.jpg](../public/images/ch5_roles_and_users_table.jpg)

- 删除所有数据库表可执行 `db.drop_all()` 函数
### 插入
- 插入记录前可以先创建一些对象
    ```
        >>> from hello import Role, User
        >>> admin= Role(name='Admin')
        >>> mod = Role(name='Moderator')
        >>> user = Role(name='User')
        >>> john = User(username='john', role=admin)
        >>> susan = User(username='susan', role=user)
        >>> david = User(username='david', role=user)
    ```
    - 此时成功创建的对象只存在于 `Python` 中，并未写入数据库，`id` 还未赋值（即便在创建对象时给 `id` 赋值，也并未与数据库中的记录对应）
    - 通过数据库会话管理对数据库所做的改动，在 `Flask-SQLAlchemy` 中会话由 `db.session` 表示
    - 准备把对象写入数据库之前，先要使用  `db.session.add()` 函数将其加入到会话中
        ```
            >>> db.session.add(admin)
            >>> db.session.add(mod)
            >>> db.session.add(user)
            >> db.session.add(john)
            >> db.session.add(susan)
            >> db.session.add(david)
        ```
    - 或使用 `db.session.add_all()` 方法添加对象列表
    - 调用 `db.session.commit()` 方法提交会话，把改动写入到数据库
    - 提交会话之后，再次查看 `id` 属性，此时 `id` 属性与数据库中记录的 `id` 值是对应的

        ![roles_and_users](../public/images/ch5_roles_and_users.jpg)
        
    - 数据库会话能够保持数据库的一致性，提交操作使用原子方式将会话中的对象全部写入数据库，能够避免因部分更新导致的数据库不一致性
### 修改
- 对对象属性进行修改后，通过调用 `db.session.add()` 方法将改动添加到会话，调用 `db.session.commit()` 方法将改动写入到数据库
### 删除
- 使用数据库会话的 `delete()` 方法删除行，调用此方法也只是将改动写入会话，还需要调用 `db.session.commit()` 方法将改动写入到数据库
### 查询
- `Flask-SQLAlchemy` 为每个模型类都提供了 `query` 对象用于查询记录
- 最基本的查询是调用 `query` 对象的 `all()` 方法取回对应表中的所有记录：`Role.query.all()`
- 使用过滤器可以配置 `query` 对象用于更精准的查询记录
    - `filter_by()`：指定查询条件
    - `limit()`：指定查询记录条数
    - `offset()`：偏移元查询返回的结果
    - `order_by()`：根据指定条件对查询结果进行排序
    - `group_by()`：根据指定条件对查询结果进行分组
    - 在查询对象上应用过滤器后，调用 `all()` 方法执行查询，返回满足条件的结果
- 除了 `all()` 方法以外，还有其他查询的执行函数：
    - `first()`：返回查询的第一个结果，如果没有结果，返回 `None`
    - `first_or_404()`：返回查询的第一个结果，如果没有结果，终止请求，返回 `404` 错误响应
    - `get()`：返回指定主键对应的行，如果没有，返回 `None`
    - `get_or_404`：返回指定主键对应的行，如果没有，终止请求，返回 `404` 错误响应
    - `count()`：返回查询结果数量
    - `paginate()`：返回一个 `Paginate` （分页）对象，包含指定范围内的结果
## 在视图函数中操作数据库
- 在视图函数中对用户通过表单提交的 `name` 数据进行唯一性验证，如果不存在，将数据写入数据库
    ```
        # hello.py
        @app.route('/', methods=['GET', 'POST'])
        def index():
            form = NameForm()
            if request.method == 'POST':
                # 首先查询表单提交的用户名是否已存在（用户名唯一性验证）
                user = User.query.filter_by(username=form.name.data).first()
                # 不存在则将表单提交的用户写入数据库
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
    ```
    ```
        # templates/index.html
        {% extends 'base.html' %}
        {% block title %}Flasky{% endblock %}
        {% block page_content %}
        <div class="page-header">
            <h1>Hello, {% if name %}{{name}}{% else %}Stranger{% endif %}!</h1>
            {% if not known %}
                <p>Pleased to meet you!</p>
            {% else %}
                <p>Happy to see you again!</p>
            {% endif %}
        </div>
        <form action="{{url_for('index')}}" method="POST">
            {{form.csrf_token}}
            <div class="form-group">
                <label for="name">{{form.name.label.text}}</label>
                {% if form.name.data %}
                    <input type="text" class="form-control" id="name" name="name" value="{{form.name.data}}"/>
                {% else %}
                    <input type="text" class="form-control" id="name" name="name"/>
                {% endif %}
            </div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="{{form.submit.label.text}}" />
            </div>
        </form>
        {% endblock %}
    ```
## 使用 Flask-Migrate 实现数据库迁移
- 参考：
    - `flask-Migrate` 文档 [Flask-Migrate文档](https://flask-migrate.readthedocs.io/en/latest)
- `Flask-Migrate` 是一个扩展，使用 `Alembic` 框架来处理 `SQLAlchemy` 数据库迁移
- 可以通过 `Flask-Cli` 命令行接口或者 `Flask-Script` 扩展来操作数据库
### 安装
- 使用 `pip` 安装
    `pip install Flask-Migrate`
### 示例
- 通过 `Flask-Migrate` 处理 `Flask` 应用的数据库迁移
    ```
        # hello.py
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_migrate import Migrate

        app = flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:test123@192.168.18.16/testdb'
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        db = SQLAlchemy(db)
        migrate = Migrate(db, migrate)
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
    ```
### 创建迁移仓库
- 使用如下命令创建一个迁移仓库：`$ flask db init`，命令执行成功后会在应用目录下生成一个 `migrations` 目录，所有的迁移脚本都会存放在这个目录中
### 创建迁移脚本
- 使用 `$ flask db migrate` 生成初始迁移脚本，命令执行成功后在 `migrateions/versions` 目录下生成一个迁移脚本，同时在数据库中会生成一个 `alembic_version` 数据表用于存储迁移记录
- 迁移脚本中有两个重要的函数： `upgrade()` 和 `downgrade()`，其中 `upgrade()` 函数把迁移脚本中的改动应用到数据库，`downgrade()` 函数则将改动回滚
    ```
        # 初始迁移脚本文件
        from alembic import op
        import sqlalchemy as sa
        def upgrade():
            # ### commands auto generated by Alembic - please adjust! ###
            op.create_table('roles',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=64), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name')
            )
            op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=64), nullable=True),
            sa.Column('role_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
            sa.PrimaryKeyConstraint('id')
            )
            op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
            # ### end Alembic commands ###


        def downgrade():
            # ### commands auto generated by Alembic - please adjust! ###
            op.drop_index(op.f('ix_users_username'), table_name='users')
            op.drop_table('users')
            op.drop_table('roles')
            # ### end Alembic commands ###
    ```
### 更新数据库
- 使用 `$ flask db upgrade` 将迁移脚本中的改动应用的数据库
- 每次数据库模型更改时都要重复使用 `migrate` 和 `upgrade` 命令

[上一章 Web 表单](../Chapter4/note.md)

[下一章 电子邮件](../Chapter6/note.md)