import json
from src.schemas import User, Coupon, Event


def db_register_user(user: User, conn, cursor):
    try:
        cursor.execute(
            f'INSERT INTO users (user_id, birthyear, country, currency, gender, registration_date) VALUES (%s, %s, %s, %s, %s, %s)',
            (user.user_id, user.birth_year, user.country, user.currency, user.gender, user.registration_date))
        conn.commit()
    except Exception as e:
        print(e)


def db_register_coupon(coupon: Coupon, conn, cursor):
    try:
        cursor.execute(f'INSERT INTO coupons (coupon_id, user_id, stake, timestamp) VALUES (%s, %s, %s, %s)',
                       (coupon.coupon_id, coupon.user_id, coupon.stake, coupon.timestamp))

        for selection in coupon.selections:
            cursor.execute(f'INSERT INTO selections (coupon_id, event_id, stake) VALUES (%s, %s, %s)',
                           (coupon.coupon_id, selection.event_id, selection.stake))
        conn.commit()
    except Exception as e:
        print(e)


def db_register_event(event: Event, conn, cursor):
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


def findUser(user_id, cursor):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", user_id)
    user = cursor.fetchone()
    if not user:
        return None
    else:
        return user


def getUserEvents(user_id, cursor):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", user_id)
    user = cursor.fetchone()
    if not user:
        return None

    cursor.execute("""
            SELECT e.* FROM events e
            JOIN selections s ON e.event_id = s.event_id
            JOIN coupons c ON s.coupon_id = c.coupon_id
            WHERE c.user_id = %s
        """, (user_id,))
    return cursor.fetchall()


def findSimilarEvents(user_id, events, cursor):
    for event in events:
        cursor.execute("""
            SELECT * FROM events
            WHERE (league = %s OR sport = %s) AND event_id != %s
            AND event_id NOT IN (SELECT event_id FROM selections WHERE coupon_id IN
            (SELECT coupon_id FROM coupons WHERE user_id = %s))
        """, (event['league'], event['sport'], event['event_id'], user_id))
        return cursor.fetchall()
