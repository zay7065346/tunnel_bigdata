#encoding: utf-8
import os


DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'tunnel_bigdata'
USERNAME = 'root'
PASSWORD = '7065346'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD,HOSTNAME,PORT,
                                                              DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True



