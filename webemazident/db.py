from pymongo import MongoClient
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = MongoClient(current_app.config['CONNECTION_STRING']).get_database(current_app.config['DATABASE'])
    return g.db