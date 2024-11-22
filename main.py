import os

from flask_login import login_user, logout_user, current_user, LoginManager
from werkzeug.security import check_password_hash

from dotenv import load_dotenv
load_dotenv()

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
	return render_template("index.html")

@app.route('/register', methods=["POST", "GET"])
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit():
		#does the user already exist?
		if data_manager.get_user(form.username.data):
			flash("Email already exists. Log in instead:")
			return redirect(url_for("login"))

		data_manager.create_and_login_user(form)
		return redirect(url_for("index"))
	return render_template("register.html", form=form)

@app.route('/login', methods=["POST","GET"])
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		user = data_manager.get_user(form.username.data)
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				return redirect(url_for("index"))
			else:
				flash("Incorrect Password")
		else:
			flash("No user found for that email")
	return render_template("login.html", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)