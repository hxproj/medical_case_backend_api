import httplib
import json
import flask
from flask import request
from sqlalchemy import func

from src import app
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
        ul=ul.get_dict()
        temp_user_list.append(ul)

    for temp in temp_user_list:

        tooth_list = Tooth_location.query.filter_by(user_id=temp['user_id']).all()
        temp_tooth_list=[]
        for tll in  tooth_list:
            tll=tll.get_dict()
            temp_tooth_list.append(tll)
        temp['tootn_location_list']=temp_tooth_list
    count = db.session.query(func.count(User.user_id)).all()[0][0]
    return_res = {'pages':count,'info_list':temp_user_list}
    ret = flask.Response(json.dumps(return_res))
    ret.headers['Access-Control-Allow-Origin'] = '*'
    return ret