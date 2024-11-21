import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase
from google.cloud.sql.connector import Connector

DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]

def get_database_url():
    url = URL.create(
    drivername="postgresql",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=os.environ["DATABASE_HOST"],
    port=5432,
    database=DATABASE_NAME)
    print(url)
    return url

def get_connection():
    connector = Connector()

    def getconn():
        conn = connector.connect(
            os.environ["CLOUD_SQL_CONNECTION_NAME"],
            driver="pg8000",
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            db=DATABASE_NAME,
        )
        return conn

    return create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

class Config:
    environment = os.environ["FLASK_ENV"]
    if environment == "development":
        SQLALCHEMY_DATABASE_URI = get_database_url()
    else:
        SQLALCHEMY_DATABASE_URI = get_connection()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f"environment is '{environment}', using SQLALCHEMY_DATABASE_URI = {SQLALCHEMY_DATABASE_URI}")

#Set up the database
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)