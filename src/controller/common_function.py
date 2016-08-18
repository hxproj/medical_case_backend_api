from src.entity.user import User

def check_if_user_exist(user_id) :
    user = User.query.filter_by(user_id=user_id).all()
    if len(user) < 1:
        return False
    else:
        return True