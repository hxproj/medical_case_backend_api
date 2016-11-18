import shutil
from datetime import datetime

from sqlalchemy import and_
import os
from src import app
from src.entity.prognosis_of_management import Prognosis_of_management
from src.entity.user import User
from src.entity.tooth_location import Tooth_location
from src import db
import copy


def check_if_user_exist(user_id):
    user = User.query.filter_by(user_id=user_id).all()
    if len(user) < 1:
        return False
    else:
        return True


def refresh_step(tooth_id, step, tooth_location=None):
    if tooth_location:
        db.session.query(Tooth_location).filter(
            and_(Tooth_location.tooth_id == (int)(tooth_id), Tooth_location.tooth_location == tooth_location)).update(
            {'step': step})
    else:
        tooth = Tooth_location.query.filter_by(tooth_id=tooth_id).first()
        word = ''
        if tooth:
            tooth_step_list = tooth.step.split(',')
            if '' in tooth_step_list:
                tooth_step_list.remove('')
            num_list =[]
            for i in range(len(tooth_step_list)):
                num_list.append((int)(tooth_step_list[i]))
            step_set = set(num_list)
            if not step in step_set:
                num_list = list(step_set)
                num_list.append(step)
                num_list.sort()
                new_tooth_list = []
                for i in range(len(num_list)):
                    new_tooth_list.append((str)(num_list[i]))
                word = reduce(lambda x,y:x+','+y,new_tooth_list)+','
            db.session.query(Tooth_location).filter(
                Tooth_location.tooth_id == (int)(tooth_id)).update(
                {'step': word})
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

def delete_directory(tooth_id):
    path = app.config['STATIC_FILES_PATH'] + (str)(tooth_id)
    if os.path.exists(path):
        shutil.rmtree(path)

def get_user_info_list(user_id_list):
    user_list = []
    for user_id in user_id_list:
        user_item = User.query.filter_by(user_id=user_id).first()
        if user_item:
            now_day = datetime.now().day
            now_month = datetime.now().month
            old_day = user_item.in_date.day
            old_month=user_item.in_date.month
            days = (now_month-old_month)*30+(now_day-old_day)
            prognosis_of_management = Prognosis_of_management.query.filter_by(user_id=user_id).first()
            if_over_date = False
            if prognosis_of_management:
                type = prognosis_of_management.patient_type
                subed_days=0
                if type == 1:
                    subed_days=days-180
                elif type ==2:
                    subed_days=days-120
                else:
                    subed_days=days-90
                if subed_days>0:
                    if_over_date=True
            user_item = user_item.get_dict()
            user_item['if_over_date']=if_over_date
            user_list.append(user_item)
    for temp in user_list:
        user_tooth_list = []
        tooth_info = Tooth_location.query.filter_by(user_id = temp['user_id']).all()
        for tooth in tooth_info:
            temp_tooth=copy.deepcopy(tooth)
            user_tooth_list.append(temp_tooth.get_dict())
        temp['tooth_location_list'] = user_tooth_list
    return user_list
