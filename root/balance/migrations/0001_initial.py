# Generated by Django 2.0.2 on 2019-01-15 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('serial_number', models.IntegerField(default=0)),
                ('transaction_amount', models.IntegerField(default=0)),
                ('transaction_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('wallet_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=10)),
                ('balance', models.IntegerField(default=3000)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='trading_wallet_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_trading_wallet', to='balance.Wallet'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_transaction_type', to='balance.TransactionType'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_wallet', to='balance.Wallet'),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together={('wallet_id', 'serial_number')},
        ),
    ]
