# Generated by Django 5.1.7 on 2025-04-03 08:17


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountHistory',
            fields=[
                ('account_history_id', models.AutoField(primary_key=True, serialize=False, verbose_name='이체내역 아이디')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='이체 금액')),
                ('type', models.CharField(choices=[('DEPOSIT', '입금'), ('WITHDRAWAL', '출금'), ('TRANSFER', '이체')], max_length=20, verbose_name='이체 타입')),
                ('amount_date', models.DateTimeField(auto_now_add=True, verbose_name='이체 날짜')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='비고')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='삭제일')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='account.account', verbose_name='계좌 아이디')),
            ],
            options={
                'verbose_name': '이체내역',
                'verbose_name_plural': '이체내역',
                'db_table': 'account_history',
                'ordering': ['-amount_date'],
            },
        ),
    ]
