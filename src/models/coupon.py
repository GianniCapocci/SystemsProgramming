from src.database.database import db


class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coupon_id = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id'))
    stake = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Date, nullable=False)
    selections = db.Column(db.JSON, nullable=False)

    user = db.relationship("User", back_populates="coupons")

    def to_dict(self):
        return {
            'id': self.id,
            'coupon_id': self.coupon_id,
            'user_id': self.user_id,
            'stake': self.stake,
            'timestamp': self.timestamp.isoformat(),
            'selections': self.selections
        }
