import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from google.cloud.sql.connector import Connector

def get_connection():
    connector = Connector()
    instance_connection=os.getenv("CLOUDSQL_CONNECTION_NAME")
    user=os.getenv("CLOUDSQL_USER")
    database=os.getenv("CLOUDSQL_DATABASE")
    print("Connecting to DB with:", {
        "connection_name": instance_connection,
        "user": user,
        "db": database})
    return connector.connect(
        instance_connection,
        "pg8000",
        user=user,
        password=os.getenv("CLOUDSQL_PASSWORD"),
        db=database,
    )

def get_database_url():
    """
    :return: a url in the format drivername://username:password@host:port/database_name
    """
    environment = os.environ["FLASK_ENV"]
    if environment == "development":
        url_str = (os.environ["DATABASE_DRIVER"] + "://" +
                   os.environ["DATABASE_USER"] + ":" + os.environ["DATABASE_PASSWORD"] + "@" +
                   os.environ["DATABASE_HOST"] + ":5432/" +
                   os.environ["DATABASE_NAME"])
    else:
        url_str = "postgresql+pg8000://"
        # host_and_port = f"/cloudsql/{os.getenv('CLOUD_SQL_CONNECTION_NAME')}"
        # host_and_port = os.environ['CLOUD_SQL_CONNECTION_NAME']
        # user_str = os.environ["DATABASE_USER"] #no password needed when using google service accounts

    print(f"environment is '{environment}', using SQLALCHEMY_DATABASE_URI = {url_str}")
    return url_str

class Config:
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if os.environ["FLASK_ENV"] == 'production':
        SQLALCHEMY_ENGINE_OPTIONS = {"creator": get_connection}

#Set up the database
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)