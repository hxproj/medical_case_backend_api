import json
import flask
from src import app
from src.controller.common_function import get_user_info_list
from src.entity.tooth_location import Tooth_location
from src.entity.user import User
from src import db
@app.route('/medical-case-of-illness/index-info-stepless',methods=['GET'])
def get_index_stepless():
    tooth_list=db.session.query(Tooth_location).filter(Tooth_location.step.in_([0,1,2,3,4,5])).all()
    stepless_userid_set=set([])
    for tooth_item in tooth_list:
        tooth_item=tooth_item.__dict__
        user_id=tooth_item['user_id']
        stepless_userid_set.add(user_id)
    user_list = get_user_info_list(stepless_userid_set)
    ret = flask.Response(json.dumps(user_list))
    ret.headers['Access-Control-Allow-Origin'] = '*'
    return ret




