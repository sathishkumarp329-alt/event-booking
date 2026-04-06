from flask import Blueprint, render_template
import pymysql
from config import Config

events_bp = Blueprint('events', __name__)

def get_db():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

@events_bp.route('/')
def index():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM events WHERE event_date > NOW() ORDER BY event_date ASC")
        events = cursor.fetchall()
    return render_template('index.html', events=events)

@events_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
    return render_template('event_detail.html', event=event)