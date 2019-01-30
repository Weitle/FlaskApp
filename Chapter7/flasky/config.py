# 应用配置选项

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or b"\xef\xe2\xe9\xfaM\xca)\x13\xb8\xf0'\t\xba\x923\xec?G\x88\x8c\x17\xaf@G0\x91^\xc7\r\xd0\xca\xfe"
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
