import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration:
    DEBUG=False
    API_PREFIX='/api/v1'
    SECRET_KEY='NyqhkvgNyqWo_RIgP-QuqNvYqA141x7CJr1lfhJ8t4g='
    SQLITE_DB_DIR = os.path.join(basedir, "../../db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "grocery_management_db.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False