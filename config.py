from pymongo import MongoClient

DATABASE = MongoClient()['DjangoTest'] # DB_NAME
DEBUG = True
client = MongoClient('localhost', 27017)