from flask import Flask
from config import Config
import pymysql

app = Flask(__name__)
app.config.from_object(Config)

def get_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

from routes.auth import auth_bp
from routes.events import events_bp
from routes.bookings import bookings_bp

app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)
app.register_blueprint(bookings_bp)

if __name__ == '__main__':
    app.run(debug=True)