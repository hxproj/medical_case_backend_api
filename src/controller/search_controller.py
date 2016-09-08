import httplib
import json

import datetime
import flask
from flask import request
from src import app
from src.controller.common_function import check_if_user_exist, get_user_info_list
from src.entity.diagnose import Diagnose
from src.entity.difficulty_assessment import Difficulty_assessment
from src.entity.illness_history import Illness_history
from src.entity.oral_examination import Oral_examination
from src.entity.personal_history import Personal_history
from src.entity.prognosis_of_management import Prognosis_of_management
from src.entity.risk_assessment import Risk_assessment
from src import db
from src.entity.tooth_location import Tooth_location


@app.route('/medical-case-of-illness/search-by-conditons',methods=['GET'])
def search_options():
    args = request.args.to_dict()
    table = args['table']
    page = args['page']
    del args['table']
    del args['page']
    query = ''
    if table =='personal_history':
        query = Personal_history.query
    elif table =='diagnose':
        query = Diagnose.query
    elif table == 'difficulty_assessment':
        query = Difficulty_assessment.query
    elif table == 'illness_history':
        query = Illness_history.query
    elif table == 'oral_examination':
        query = Oral_examination.query
    elif table == 'prognosis_of_management':
        query = Prognosis_of_management.query
    elif table == 'tooth_location':
        query = Tooth_location.query
    result_list = query.filter_by(**args).all()
    user_id_list = []
    for result in result_list:
        user_id_list.append(result.user_id)
    result = get_user_info_list(user_id_list)
    if page =='' or page ==None:
        response = flask.Response((str)(len(result)))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response,200
    else:
        try:
            if (int)(page)== 0:
                offset_start =0
            else:
                offset_start =(int)(page)*app.config['PER_PAGE']-1
            offset_end = offset_start+app.config['PER_PAGE']
            if offset_end>len(result):
                return_list = result[offset_start:-1]
                return_list.append(result[-1])
            else:
                return_list = result[offset_start:offset_end]
            response = flask.Response(json.dumps(return_list))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        except:
            response = flask.Response('out of range')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400