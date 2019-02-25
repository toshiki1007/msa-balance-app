from django.test import TestCase
from .models import *
from django.test import Client
import json
from django.urls import reverse

class WalletTests(TestCase):
	@classmethod
	def setUpTestData(self):
		Wallet.objects.create(user_id = 'buyer', balance = 1000)
		Wallet.objects.create(user_id = 'seller', balance = 100000)

		TransactionType.objects.create(type_name = '送金')
		TransactionType.objects.create(type_name = '着金')
		TransactionType.objects.create(type_name = '購入')
		TransactionType.objects.create(type_name = '売却')

	def test_get_response(self):
		url = reverse('update')
		res = self.client.get(url).json()
		self.assertEqual (res['statusCode'], 400)
		self.assertEqual (res['message'], 'invalid access error')

	def test_buy_success(self):
		url = reverse('update')
		data = {
			"userId":"buyer",
			"tradingUserId":"seller",
			"price":"100",
			"typeFlg":"1"
		}
		res = self.client.post(url, content_type='application/json', data=json.dumps(data)).json()
		self.assertEqual (res['statusCode'], 200)
		self.assertEqual (res['message'], 'success')
		
	def test_buy_fail(self):
		url = reverse('update')
		data = {
			"userId":"buyer",
			"tradingUserId":"seller",
			"price":"100",
			"typeFlg":"1"
		}
		res = self.client.post(url, content_type='application/json', data=json.dumps(data)).json()
		self.assertEqual (res['statusCode'], 400)
		self.assertEqual (res['message'], 'insufficient balance error')

	def test_remittance_success(self):
		url = reverse('update')
		data = {
			"userId":"buyer",
			"tradingUserId":"seller",
			"price":"100",
			"typeFlg":"0"
		}
		res = self.client.post(url, content_type='application/json', data=json.dumps(data)).json()
		self.assertEqual (res['statusCode'], 200)
		self.assertEqual (res['message'], 'success')

	def test_remittance_fail(self):
		url = reverse('update')
		data = {
			"userId":"buyer",
			"tradingUserId":"seller",
			"price":"10000",
			"typeFlg":"0"
		}
		res = self.client.post(url, content_type='application/json', data=json.dumps(data)).json()
		self.assertEqual (res['statusCode'], 400)
		self.assertEqual (res['message'], 'insufficient balance error')
