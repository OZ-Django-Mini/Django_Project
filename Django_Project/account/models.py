import uuid
from django.db import models
from django.conf import settings

class Account(models.Model):

    account_id = models.AutoField(
        primary_key=True,
        editable=False,
        db_column='account_id'
    )

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='account'
    )

    #계좌 번호
    account_number =  models.UUIDField(
        editable=False,
        db_column='account_number'
    )

    # 잔액
    balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='balance')

    # 생성 시각
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        db_column='created_at')

    # 삭제 시각
    deleted_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        db_column='deleted_at')

    def __str__(self):
        return f"{self.account_number} ({self.user_id})"

    class Meta:
        db_table = 'account'
