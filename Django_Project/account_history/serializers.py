# account_history/serializers.py
# API 요청과 응답을 위한 직렬화/역직렬화 클래스 정의

from rest_framework import serializers
from .models import AccountHistory
from account.models import Account
from decimal import Decimal


class AccountHistorySerializer(serializers.ModelSerializer):
    """계좌 거래 내역 기본 시리얼라이저"""

    # 추가 필드
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    account_number = serializers.CharField(source='account.account_number', read_only=True)
    username = serializers.CharField(source='user.email', read_only=True)


    class Meta:
        model = AccountHistory
        fields = (
            'account_history_id', 'account', 'account_number', 'user', 'username',
            'amount', 'type', 'type_display', 'amount_date', 'description'
        )
        read_only_fields = ('account_history_id', 'amount_date')


class AccountHistoryUpdateSerializer(serializers.ModelSerializer):
    """거래 내역 수정을 위한 시리얼라이저 (설명만 수정 가능)"""

    class Meta:
        model = AccountHistory
        fields = ('description',)


class AccountHistoryFilterSerializer(serializers.Serializer):
    """거래 내역 필터링을 위한 시리얼라이저"""

    account_id = serializers.IntegerField(required=False)
    type = serializers.ChoiceField(choices=AccountHistory.TYPE_CHOICES, required=False)
    min_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)