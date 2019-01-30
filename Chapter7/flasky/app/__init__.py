from flask import Flask

from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 导入并初始化 db 实例
    from .db import db
    db.init_app(app)

    #@app.route('/')
    #def index():
    #    return 'Hello World'
    # 使用蓝本实现功能
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app