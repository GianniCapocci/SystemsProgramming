import json

from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from schemas import User, Coupon, Event

mysql = MySQL()

app = Flask(__name__)

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


def db_register_user(user: User):
    try:
        cursor.execute(
            f'INSERT INTO users (user_id, birthyear, country, currency, gender, registration_date) VALUES (%s, %s, %s, %s, %s, %s)',
            (user.user_id, user.birth_year, user.country, user.currency, user.gender, user.registration_date))
        conn.commit()
    except Exception as e:
        print(e)


def db_register_coupon(coupon: Coupon):
    try:
        cursor.execute(f'INSERT INTO coupons (coupon_id, user_id, stake, timestamp) VALUES (%s, %s, %s, %s)',
                       (coupon.coupon_id, coupon.user_id, coupon.stake, coupon.timestamp))

        for selection in coupon.selections:
            cursor.execute(f'INSERT INTO selections (coupon_id, event_id, stake) VALUES (%s, %s, %s)',
                           (coupon.coupon_id, selection.event_id, selection.stake))
        conn.commit()
    except Exception as e:
        print(e)


def db_register_event(event: Event):
    try:
        insert_query = """
                        INSERT INTO events (begin_timestamp, country, end_timestamp, event_id, league, participants, sport)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """

        participants_json = json.dumps(event.participants)

        cursor.execute(insert_query, (
            event.begin_timestamp,
            event.country,
            event.end_timestamp,
            event.event_id,
            event.league,
            participants_json,
            event.sport
        ))

        conn.commit()
    except Exception as e:
        print(e)
