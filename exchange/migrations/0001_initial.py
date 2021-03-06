# Generated by Django 2.2.4 on 2019-08-25 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=50, unique=True)),
                ('price_in_usd', models.DecimalField(decimal_places=10, max_digits=18)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawalRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=10, default=0, max_digits=24)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('failed', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exchange.Coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='withdrawals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BalanceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=10, default=0, max_digits=24)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modification_type', models.CharField(choices=[('MANUAL', 'Manual modification by staff'), ('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal')], max_length=50)),
                ('payment_address', models.CharField(blank=True, max_length=255, null=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exchange.Coin')),
                ('modified_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_balance_history', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=10, default=0, max_digits=24)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exchange.Coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'coin')},
            },
        ),
    ]
