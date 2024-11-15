import os

from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["FLASK_KEY"]


bootstrap = Bootstrap5(app)

@app.route("/", methods=["GET", "POST"])
def index():
	form = BasicForm()
	if form.validate_on_submit():
		pass
	return render_template("index.html", form=form)

class BasicForm(FlaskForm):
	user_input = StringField("Input", validators=[DataRequired()])
	submit = SubmitField("Submit")

if __name__ == "__main__":
	app.run(debug=True)
