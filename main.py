import os

from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

from dotenv import load_dotenv
load_dotenv()

from coinbase.wallet.client import Client as CoinbaseClient
cb_client = CoinbaseClient(os.environ["COINBASE_API_KEY"] , os.environ["COINBASE_SECRET"])


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["FLASK_KEY"]
bootstrap = Bootstrap5(app)

crypto_list = [
	("BTC", "Bitcoin"),
	("ETH", "Ethereum"),
	("SOL", "Solana"),
]

def get_asset_price(asset):
	print(f"getting price for {asset} ...")
	currency_pair = f"{asset}-GBP"
	price_data = cb_client.get_spot_price(currency_pair=currency_pair)
	price = price_data["amount"]
	print(price)
	return price

@app.route("/", methods=["GET", "POST"])
def index():
	form = BasicForm()
	asset=""
	price=0
	if form.validate_on_submit():
		asset = form.selected.data
		price = get_asset_price(asset)
	return render_template("index.html", form=form, asset=asset, price=price)

class BasicForm(FlaskForm):
	selected = SelectField("Select asset", choices=crypto_list)
	submit = SubmitField("Submit")

if __name__ == "__main__":
	app.run(debug=True)