import os

from flask_login import login_user, logout_user, current_user, LoginManager
from werkzeug.security import check_password_hash

from dotenv import load_dotenv
load_dotenv()

import portfolio
import price_checker
from flask import Flask, render_template, redirect, url_for, flash
import forms
from data import data_manager, db

# noinspection PyPackageRequirements
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["FLASK_KEY"]

app.config.from_object(db.Config)
#
db.db.init_app(app)
data_manager.app = app

bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
	data_manager.db.create_all()

@login_manager.user_loader
def get_user_for_id(user_id):
	return data_manager.get_user_for_id(user_id)

@app.route("/", methods=["GET", "POST"])
def index():
	form = forms.PriceCheckForm()
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
	current_user_portfolio = portfolio.get_current_user_portfolio()
	if form.validate_on_submit():
		purchase = data_manager.AssetPurchase.create_from_form(form)
		current_user_portfolio.add_purchase(purchase)
		if current_user.is_authenticated:
			data_manager.save(purchase)
		current_user_portfolio = portfolio.get_current_user_portfolio() #reload from the database after the connection has been closed
	return render_template("portfolio.html", form=form, portfolio=current_user_portfolio)

@app.route('/register', methods=["POST", "GET"])
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		#does the user already exist?
		if data_manager.get_user(form.username.data):
			flash("Email already exists. Log in instead:")
			return redirect(url_for("login"))

		data_manager.create_and_login_user(form)
		return redirect(url_for("show_portfolio"))
	return render_template("register.html", form=form)

@app.route('/login', methods=["POST","GET"])
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		user = data_manager.get_user(form.username.data)
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				return redirect(url_for("show_portfolio"))
			else:
				flash("Incorrect Password")
		else:
			flash("No user found for that email")
	return render_template("login.html", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('show_portfolio'))

if __name__ == "__main__":
	app.run(debug=True)