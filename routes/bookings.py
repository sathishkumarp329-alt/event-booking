from flask import Blueprint, request, redirect, url_for, session, flash, render_template
import pymysql
from config import Config

bookings_bp = Blueprint('bookings', __name__)

def get_db():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

@bookings_bp.route('/book/<int:event_id>', methods=['POST'])
def book_ticket(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    quantity = int(request.form.get('quantity', 1))
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        if event['available_tickets'] < quantity:
            flash('Not enough tickets available.', 'danger')
            return redirect(url_for('events.event_detail', event_id=event_id))
        total = event['price'] * quantity
        cursor.execute(
            "INSERT INTO bookings (user_id, event_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
            (session['user_id'], event_id, quantity, total)
        )
        cursor.execute(
            "UPDATE events SET available_tickets = available_tickets - %s WHERE id = %s",
            (quantity, event_id)
        )
        db.commit()
    flash(f'Successfully booked {quantity} ticket(s)!', 'success')
    return redirect(url_for('bookings.my_tickets'))

@bookings_bp.route('/my-tickets')
def my_tickets():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT b.*, e.title, e.event_date, e.venue
            FROM bookings b JOIN events e ON b.event_id = e.id
            WHERE b.user_id = %s ORDER BY b.booking_date DESC
        """, (session['user_id'],))
        bookings = cursor.fetchall()
    return render_template('my_tickets.html', bookings=bookings)