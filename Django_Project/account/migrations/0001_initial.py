# Generated by Django 5.1.7 on 2025-04-03 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(db_column='account_id', editable=False, primary_key=True, serialize=False)),
                ('account_number', models.UUIDField(db_column='account_number', editable=False)),
                ('balance', models.DecimalField(blank=True, db_column='balance', decimal_places=2, max_digits=18, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('deleted_at', models.DateTimeField(auto_now=True, db_column='deleted_at', null=True)),
            ],
            options={
                'db_table': 'account',
            },
        ),
    ]
