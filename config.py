    
SECRET_KEY = 'secret-key-goes-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

DB_USER = "root"
DB_PASSWORD = "Anjostar02$"
DB_HOST = "127.0.0.1"
DB_NAME = "steam_db"

SQLALCHEMY_DATABASE_URI  = "mysql+pymysql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_HOST+"/"+DB_NAME #For mysql
