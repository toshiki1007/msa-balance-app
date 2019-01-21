from django.http.response import JsonResponse
from .models import *
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json

def response(status_code, msg):
	res_msg = {
		'message': msg
	}
	json_str = json.dumps(res_msg, ensure_ascii=False, indent=4)
	res = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status_code)

	return res

#残高更新処理
@csrf_exempt
def update(request):
	if request.method != 'POST':
		return response(400, 'invalid access error')

	params = json.loads(request.body.decode())

	user_id = params['userId']
	trading_user_id = params['tradingUserId']
	price = int(params['price'])
	type_flg = params['typeFlg']

	#type_flg==0 ⇒ 送金取引
	if type_flg == '0':
		transaction_type_flg = 1
		trading_transaction_type_flg = 2
	#type_flg==1 ⇒ 商品取引
	else:
		transaction_type_flg = 3
		trading_transaction_type_flg = 4

	wallet = Wallet.objects.get(user_id = user_id)
	wallet_id = wallet.wallet_id
	wallet_balance =  wallet.balance

	trading_wallet = Wallet.objects.get(user_id = trading_user_id)
	trading_wallet_id = trading_wallet.wallet_id
	trading_wallet_balance = trading_wallet.balance

	#残高chk
	wallet_balance =  wallet.balance
	if wallet_balance < price:
		return response(400, 'insufficient balance error')

	try:
		#残高update
		wallet.balance = wallet_balance - price
		wallet.save()

		trading_wallet.balance = trading_wallet_balance + price
		trading_wallet.save()

		serial_number = Transaction.objects.filter(wallet_id = wallet_id).aggregate(Max('serial_number'))['serial_number__max']
		if serial_number == None:
			serial_number = 0

		tradning_serial_number = Transaction.objects.filter(wallet_id = trading_wallet_id).aggregate(Max('serial_number'))['serial_number__max']
		if tradning_serial_number == None:
			tradning_serial_number = 0

		#履歴create
		buyer_transaction = Transaction.objects.create(
			wallet_id = wallet,
			serial_number = serial_number + 1,
			trading_wallet_id = trading_wallet,
			transaction_type = TransactionType.objects.get(id = transaction_type_flg),
			transaction_amount = -price,
		)

		seller_transaction = Transaction.objects.create(
			wallet_id = trading_wallet,
			serial_number = tradning_serial_number + 1,
			trading_wallet_id = wallet,
			transaction_type = TransactionType.objects.get(id = trading_transaction_type_flg),
			transaction_amount = price,
		)
	except:
		return response(400, 'invalid update balance error')

	return response(200, 'success')