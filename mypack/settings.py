DEBUG = False
SERVER_NAME = 'mycomputer.com'

DB_USER = "travis"
DB_PASS = ""
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "sakila"

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
