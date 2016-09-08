from sqlalchemy import and_
import os
from src import app
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


def check_directory(tooth_id):
    path = app.config['STATIC_FILES_PATH'] + (str)(tooth_id)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def check_file(tooth_id, file_name):
    path = app.config['STATIC_FILES_PATH'] + (str)(tooth_id) + '\\' + file_name
    if not os.path.exists(path):
        return False, path
    else:
        return True, path


def get_user_info_list(user_id_list):
    user_list = []
    for user_id in user_id_list:
        user_item = User.query.filter_by(user_id=user_id).first()
        user_item = user_item.get_dict()
        user_list.append(user_item)
    for temp in user_list:
        user_tooth_list = []
        tooth_info = Tooth_location.query.filter_by(user_id = temp['user_id']).all()
        for tooth in tooth_info:
            user_tooth_list.append(tooth.get_dict())
        temp['tooth_location_list'] = user_tooth_list
    return user_list
