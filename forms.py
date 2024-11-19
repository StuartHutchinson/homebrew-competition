from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired

from portfolio import CRYPTO_LIST

class PriceCheckForm(FlaskForm):
    assets = SelectMultipleField("Select asset(s)", choices=CRYPTO_LIST)
    submit = SubmitField("Check Prices")

class PurchaseForm(FlaskForm):
    asset = SelectField("Select asset", choices=CRYPTO_LIST, validators=[DataRequired()])
    purchase_price = FloatField("Asset price", validators=[DataRequired()])
    gbp = FloatField("Purchase price £")
    submit = SubmitField("Add")