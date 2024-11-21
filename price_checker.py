import os

from coinbase.wallet.client import Client as CoinbaseClient
cb_client = CoinbaseClient(os.environ["COINBASE_API_KEY"] , os.environ["COINBASE_SECRET"])

def get_asset_price(asset):
	print(f"getting price for {asset} ...")
	currency_pair = f"{asset}-GBP"
	price_data = cb_client.get_spot_price(currency_pair=currency_pair)
	price = price_data["amount"]
	print(price)
	return float(price)