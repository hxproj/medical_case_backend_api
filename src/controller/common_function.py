from sqlalchemy import and_

from src.entity.user import User
from src.entity.tooth_location import Tooth_location
from src import db


def check_if_user_exist(user_id):
    user = User.query.filter_by(user_id=user_id).all()
    if len(user) < 1:
        return False
    else:
        return True


def refresh_step(user_id, step, tooth_location=None):
    if tooth_location:
        db.session.query(Tooth_location).filter(
            and_(Tooth_location.user_id == user_id, Tooth_location.tooth_location == tooth_location)).update(
            {'step': step})
    else:
        db.session.query(Tooth_location).filter(
            Tooth_location.user_id == user_id).update(
            {'step': step})
    db.session.commit()
