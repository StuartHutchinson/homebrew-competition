from flask import Flask
from flask_login import login_user
from werkzeug.security import generate_password_hash

from data.db import db
from entities import User, AssetPurchase

app: Flask #this is set in main.py when initialising

CRYPTO_LIST = [
	("BTC", "Bitcoin"),
	("ETH", "Ethereum"),
	("SOL", "Solana"),
]

def save(entity):
    with app.app_context():
        db.session.add(entity)
        db.session.commit()

def get_user(username):
    return db.session.execute(db.select(User).where(User.username == username)).scalar()

def get_user_for_id(user_id):
    return db.session.get(User, user_id)

def create_and_login_user(form):
    hashed_pwd = generate_password_hash(form.password.data)
    user = User(username=form.username.data, password=hashed_pwd)
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        print(f"Registered new user <{user.id}>")
        login_user(user)

def get_purchases_for_user(user_id):
    with app.app_context():
        return db.session.execute(db.select(AssetPurchase).where(AssetPurchase.owner_id == user_id)).scalars().all()