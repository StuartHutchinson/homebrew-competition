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
	form = forms.PriceCheckForm()
	asset=""
	price_str="Current prices:\n"
	if form.validate_on_submit():
		assets = form.assets.data
		for asset in assets:
			price = price_checker.get_asset_price(asset)
			price_str += f"{asset} - £{'{:.2f}'.format(price)}\n"
	return render_template("index.html", form=form, price_str=price_str)

@app.route("/portfolio", methods=["GET", "POST"])
def show_portfolio():
	form = forms.PurchaseForm()
	if form.validate_on_submit():
		portfolio.add_asset(form)
	return render_template("portfolio.html", form=form, portfolio=portfolio.portfolio)

if __name__ == "__main__":
	app.run(debug=True)