import httplib
import json

from datetime import datetime
import flask
from flask import request
from sqlalchemy import func

from src import app
from src.entity.prognosis_of_management import Prognosis_of_management
from src.entity.tooth_location import Tooth_location
from src.entity.user import User
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db

@app.route('/medical-case-of-illness/index-info',methods=['GET'])
def get_index():
    page = request.args.get('page',1,type=int)
    offset = (page-1)*app.config['PER_PAGE']
    query = db.session.query(User).order_by(User.user_id.desc())
    query = query.offset(offset)
    query = query.limit(app.config['PER_PAGE'])
    user_list =query.all()
    temp_user_list=[]
    for ul in user_list:
        now_day = datetime.now().day
        now_month = datetime.now().month
        old_day = ul.in_date.day
        old_month = ul.in_date.month
        days = (now_month - old_month) * 30 + (now_day - old_day)
        prognosis_of_management = Prognosis_of_management.query.filter_by(user_id=ul.user_id).first()
        if_over_date = False
        if prognosis_of_management:
            type = prognosis_of_management.patient_type
            subed_days = 0
            if type == 1:
                subed_days = days - 180
            elif type == 2:
                subed_days = days - 120
            else:
                subed_days = days - 90
            if subed_days > 0:
                if_over_date = True
        ul=ul.get_dict()
        ul['if_over_date']=if_over_date
        temp_user_list.append(ul)
    for temp in temp_user_list:

        tooth_list = Tooth_location.query.filter_by(user_id=temp['user_id']).all()
        temp_tooth_list=[]
        for tll in  tooth_list:
            tll=tll.get_dict()
            temp_tooth_list.append(tll)
        temp['tootn_location_list']=temp_tooth_list
    count = db.session.query(func.count(User.user_id)).all()[0][0]
    count = count/app.config['PER_PAGE']+1
    return_res = {'pages':count,'info_list':temp_user_list}
    ret = flask.Response(json.dumps(return_res))
    ret.headers['Access-Control-Allow-Origin'] = '*'
    return ret