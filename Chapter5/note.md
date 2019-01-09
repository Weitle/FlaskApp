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

