import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQALCHEMY_TRACK_NOTIFICATIONS = False

class LocalDevelopementConfig(Config):
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(basedir, "../")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")