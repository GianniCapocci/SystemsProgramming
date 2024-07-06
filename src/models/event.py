from src.database.database import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.String(50), unique=True, nullable=False)
    begin_timestamp = db.Column(db.Date, nullable=False)
    end_timestamp = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    league = db.Column(db.String(50), nullable=False)
    participants = db.Column(db.JSON, nullable=False)
    sport = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'begin_timestamp': self.begin_timestamp.isoformat(),
            'end_timestamp': self.end_timestamp.isoformat(),
            'country': self.country,
            'league': self.league,
            'participants': self.participants,
            'sport': self.sport
        }
