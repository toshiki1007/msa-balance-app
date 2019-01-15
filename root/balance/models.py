from django.db import models

class Wallet(models.Model):
	wallet_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=10)
	balance = models.IntegerField(default=3000)

	def __str__(self):
		return str(self.wallet_id)

class Transaction(models.Model):
	class Meta:
		unique_together = (('wallet_id', 'serial_number'),)

	transaction_id = models.AutoField(primary_key=True)
	wallet_id = models.ForeignKey('Wallet', related_name='r_wallet', on_delete=models.CASCADE)
	serial_number = models.IntegerField(
            default=0,
            blank=False,
            null=False
		)
	trading_wallet_id = models.ForeignKey('Wallet', related_name='r_trading_wallet', on_delete=models.CASCADE)
	transaction_type = models.ForeignKey('TransactionType', related_name='r_transaction_type', on_delete=models.CASCADE)
	transaction_amount = models.IntegerField(default=0)
	transaction_date = models.DateTimeField(
            auto_now=True,
            blank=False,
            null=False
		)

	def __str__(self):
		return str(self.wallet_id) + ' : ' + str(self.serial_number)

class TransactionType(models.Model):
	type_name = models.CharField(max_length=2)

	def __str__(self):
		return str(self.type_name)