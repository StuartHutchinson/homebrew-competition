import os
import forms
import portfolio
import price_checker
from flask import Flask, abort, render_template, redirect, url_for, flash

from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["FLASK_KEY"]
bootstrap = Bootstrap5(app)

@app.route("/", methods=["GET", "POST"])
def index():
	form = forms.BasicForm()
	asset=""
	price=0
	if form.validate_on_submit():
		asset = form.asset.data
		price = price_checker.get_asset_price(asset)
	return render_template("index.html", form=form, asset=asset, price=price)

@app.route("/portfolio", methods=["GET", "POST"])
def show_portfolio():
	form = forms.PurchaseForm()
	if form.validate_on_submit():
		asset = form.asset.data
		purchase_price = form.purchase_price.data
		gbp = form.gbp.data
		crypto_amount = gbp/purchase_price
		portfolio.add_asset(asset, crypto_amount)
	return render_template("portfolio.html", form=form, portfolio_dict=portfolio.user_portfolio)

if __name__ == "__main__":
	app.run(debug=True)