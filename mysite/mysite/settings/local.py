from .base import *

# 开发环境设置
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 数据库设置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}