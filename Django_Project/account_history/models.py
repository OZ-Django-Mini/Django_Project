# account_history/models.py
# 이체내역(거래 내역) 모델을 정의하는 파일입니다.

from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import Account
from user.models import CustomUser

class AccountHistory(models.Model):
    """계좌 거래 내역 모델

    이체, 입금, 출금 등의 계좌 거래 내역을 저장합니다.
    """
    # 거래 유형 선택지
    TYPE_CHOICES = (
        ('DEPOSIT', '입금'),
        ('WITHDRAWAL', '출금'),
        ('TRANSFER', '이체'),
    )

    # 기본 필드 (데이터베이스 스키마에 맞춤)
    account_history_id = models.AutoField(primary_key=True, verbose_name=_('이체내역 아이디'))
    account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                related_name='transactions', verbose_name=_('계좌 아이디'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='transactions', verbose_name=_('사용자 아이디'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('이체 금액'))
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_('이체 타입'))
    amount_date = models.DateTimeField(auto_now_add=True, verbose_name=_('이체 날짜'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('비고'))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('삭제일'))

    class Meta:
        db_table = 'account_history'
        ordering = ['-amount_date']

    def __str__(self):
        """모델의 문자열 표현"""
        return f"{self.type} - {self.amount} - {self.amount_date.strftime('%Y-%m-%d %H:%M')}"

    def soft_delete(self):
        """소프트 삭제 메서드"""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save()

    @property
    def is_deleted(self):
        """삭제 여부 확인 속성"""
        return self.deleted_at is not None
