#API ORIENTED DATABASE CONFIGURATION
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'ScuRX0z6Nb'
app.config['MYSQL_DATABASE_PASSWORD'] = 'o6CJSRnS75'
app.config['MYSQL_DATABASE_DB'] = 'ScuRX0z6Nb'
app.config['MYSQL_DATABASE_HOST'] = 'remotemysql.com'
mysql.init_app(app)