from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    # username, password는 AbstractUser에 기본 포함되어 있음
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'  # 로그인 ID를 email로 설정
    REQUIRED_FIELDS = ['username', 'name', 'nickname', 'phone']

    def __str__(self):
        return self.email
