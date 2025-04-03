import uuid
from .models import Account
from rest_framework import serializers

class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'balance']

    def create(self, validated_data):
        account = Account.objects.create(
            user_id=validated_data['user_id'],
            balance=validated_data['balance'],
            account_number= uuid.uuid4()
            )
        return account

class AccountReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'balance']



class AccountTransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(choices=[('DEPOSIT', '입금'),
        ('WITHDRAWAL', '출금'),
        ('TRANSFER', '이체')])
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        model = Account
        fields = ['user_id', 'account_number', 'balance', 'transaction_type', 'amount']


    def update(self, instance, validated_data):
        amount = validated_data['amount']
        transaction_type = validated_data['transaction_type']

        # 입금 일때
        if transaction_type == 'DEPOSIT':
            instance.balance += amount

        # 출금 일때
        elif transaction_type == 'WITHDRAWAL':
            if instance.balance < amount:
                raise serializers.ValidationError("잔액이 부족합니다.")
            instance.balance -= amount


        instance.save()




