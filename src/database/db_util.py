from typing import List

from sqlalchemy import or_, not_
from sqlalchemy.orm import Session

from src.models.coupon import Coupon
from src.models.event import Event
from src.models.user import User


def db_register_user(user_data, session: Session):
    user = User(
        user_id=user_data.get('user_id'),
        birth_year=user_data.get('birth_year'),
        country=user_data.get('country'),
        currency=user_data.get('currency'),
        gender=user_data.get('gender'),
        registration_date=user_data.get('registration_date')
    )
    session.add(user)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def event_exists(event_id: str, session: Session) -> bool:
    event = session.query(Event).filter(Event.event_id == event_id).first()
    return event is not None


def db_register_coupon(coupon_data: Coupon, session: Session):
    coupon = Coupon(
        coupon_id=coupon_data.get('coupon_id'),
        user_id=coupon_data.get('user_id'),
        stake=coupon_data.get('stake'),
        timestamp=coupon_data.get('timestamp'),
        selections=coupon_data.get('selections')
    )
    session.add(coupon)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def db_register_event(event_data: Event, session: Session):
    event = Event(
        event_id=event_data.get('event_id'),
        begin_timestamp=event_data.get('begin_timestamp'),
        end_timestamp=event_data.get('end_timestamp'),
        country=event_data.get('country'),
        league=event_data.get('league'),
        participants=event_data.get('participants'),
        sport=event_data.get('sport')
    )
    session.add(event)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def findUser(user_id: str, session: Session):
    user = session.query(User).filter(User.user_id == user_id).first()
    return user


def userExists(user_id: str, session: Session) -> bool:
    user = session.query(User).filter(User.user_id == user_id).first()
    return user is not None


def getUserEvents(user_id: str, session: Session) -> List[dict]:
    try:
        if not userExists(user_id, session):
            return []

        coupons = session.query(Coupon).filter(Coupon.user_id == user_id).all()

        events = []
        for coupon in coupons:
            selections = coupon.selections
            if selections:
                for selection in selections:
                    event_id = selection.get('event_id')
                    event = session.query(Event).filter(Event.event_id == event_id).first()
                    if event:
                        events.append(event)

        return [event.__dict__ for event in events]

    except Exception as e:
        print(f"Exception: {e}")
        return []


def findSimilarEvents(user_id: str, session: Session) -> List[dict]:
    try:
        user_events = getUserEvents(user_id, session)
        if not user_events:
            return []

        similar_events = []
        for event_data in user_events:
            event_id = event_data['event_id']
            league = event_data['league']
            sport = event_data['sport']

            subquery = session.query(Coupon.selections).filter(Coupon.user_id == user_id).subquery()

            # Query to find similar events
            similar_events_query = session.query(Event).filter(
                or_(Event.league == league, Event.sport == sport),
                Event.event_id != event_id,
                not_(Event.event_id.in_(subquery))
            )

            results = similar_events_query.all()

            similar_events.extend([event.to_dict() for event in results])

        return similar_events

    except Exception as e:
        print(f"Exception: {e}")
        return []
    finally:
        session.close()
