from .base import * # noqa

DEBUG = False   # 디버그 모드(개발 모드) 에러가 발생 하면 장고에서 노란 화면으로 알려줌

ALLOWED_HOSTS = [
    "13.125.186.81", # EC2 퍼블릭 IP
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'instagram',
        'USER': 'dev_user',
        'PASSWORD': 'securepassword',
        'HOST': 'db',
        'PORT': '5432',
    }
}