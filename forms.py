from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, SelectField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

from data import data_manager

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PriceCheckForm(FlaskForm):
    assets = MultiCheckboxField("Select asset(s)", choices=data_manager.CRYPTO_LIST)
    submit = SubmitField("Check Prices")

class PurchaseForm(FlaskForm):
    asset = SelectField("Select asset", choices=data_manager.CRYPTO_LIST, validators=[DataRequired()])
    date = DateField("Purchase date")
    price = FloatField("Asset price", validators=[DataRequired()])
    gbp = FloatField("Purchase price £")
    fees = FloatField("Fees £")
    submit = SubmitField("Add")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")