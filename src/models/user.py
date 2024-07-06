from src.database.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)

    coupons = db.relationship("Coupon", back_populates="user")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'birth_year': self.birth_year,
            'country': self.country,
            'currency': self.currency,
            'gender': self.gender,
            'registration_date': self.registration_date
        }
