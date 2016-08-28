from src.entity.user import User
from src.entity.tooth_location import Tooth_location
from src import db

def check_if_user_exist(user_id) :
    user = User.query.filter_by(user_id=user_id).all()
    if len(user) < 1:
        return False
    else:
        return True

def refresh_step(tooth_id,step):
    db.session.query(Tooth_location).filter(Tooth_location.tooth_id==tooth_id).update({'step':step})
    db.session.commit()