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
    username = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = AccountHistory
        fields = (
            'account_history_id', 'account', 'account_number', 'user', 'username',
            'amount', 'type', 'type_display', 'amount_date', 'description'
        )
        read_only_fields = ('account_history_id', 'amount_date')


class AccountHistoryCreateSerializer(serializers.ModelSerializer):
    """거래 내역 생성을 위한 시리얼라이저"""

    account_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AccountHistory
        fields = ('account_id', 'amount', 'type', 'description')

    def validate_amount(self, value):
        """금액 유효성 검사"""
        if value <= Decimal('0'):
            raise serializers.ValidationError("금액은 0보다 커야 합니다.")
        return value

    def validate(self, data):
        """추가 유효성 검사"""
        account_id = data.get('account_id')
        amount = data.get('amount')
        history_type = data.get('type')

        try:
            account = Account.objects.get(account_id=account_id)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"account_id": "존재하지 않는 계좌입니다."})

        # 출금 및 이체 시 잔액 확인
        if history_type in ['WITHDRAWAL', 'TRANSFER'] and account.balance < amount:
            raise serializers.ValidationError({"amount": "잔액이 부족합니다."})

        # 요청 사용자가 계좌 소유자인지 확인
        request = self.context.get('request')
        if request and account.user.user_id != request.user.user_id:
            raise serializers.ValidationError({"account_id": "본인의 계좌만 이용할 수 있습니다."})

        return data

    def create(self, validated_data):
        """거래 내역 생성 및 계좌 잔액 업데이트"""
        account_id = validated_data.pop('account_id')
        account = Account.objects.get(account_id=account_id)
        user = self.context['request'].user

        # 트랜잭션 처리는 view에서 수행

        return AccountHistory.objects.create(
            account=account,
            user=user,
            **validated_data
        )


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