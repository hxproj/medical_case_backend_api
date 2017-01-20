import httplib
import json

import datetime
from operator import and_

import flask
from flask import request
from src import app
from src.controller.common_function import check_if_user_exist, get_user_info_list, calculate_age
from src.entity.diagnose import Diagnose
from src.entity.difficulty_assessment import Difficulty_assessment
from src.entity.illness_case import Illness_case
from src.entity.illness_history import Illness_history
from src.entity.oral_examination import Oral_examination
from src.entity.personal_history import Personal_history
from src.entity.prognosis_of_management import Prognosis_of_management
from src.entity.risk_assessment import Risk_assessment
from src import db
from src.entity.surgical import Surgical
from src.entity.tooth_location import Tooth_location
from src.entity.user import User
from src.entity.usphs import Usphs


@app.route('/medical-case-of-illness/search-by-conditons', methods=['GET'])
def search_options():
    args = request.args.to_dict()
    table = args['table']
    page = args['page']
    del args['table']
    del args['page']
    query = ''
    if table == 'personal_history':
        query = Personal_history.query
    elif table == 'user':
        query = User.query
    elif table == 'diagnose':
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
    elif table == 'usphs':
        query = Usphs.query
    elif table == 'surgical':
        query = Surgical.query
    elif table == 'risk_assessment':
        query = Risk_assessment.query
    se = set(['salivary_gland_disease', 'consciously_reduce_salivary_flow'])
    result_list = []
    for key in args:
        if key in se:
            result_list = _search_special(key)
        else:
            result_list = query.filter_by(**args).all()
    user_id_list = []
    for result in result_list:
        user_id_list.append(result.user_id)
    temp_set = set(user_id_list)
    user_id_list = list(temp_set)
    result = get_user_info_list(user_id_list)
    result = result[-1::-1]
    if page == '' or page == None:
        response = flask.Response((str)(len(result)))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 200
    else:
        try:
            offset_start = ((int)(page) - 1) * app.config['PER_PAGE']
            offset_end = offset_start + app.config['PER_PAGE']
            if offset_end > len(result):
                return_list = result[offset_start:-1]
                return_list.append(result[-1])
            else:
                return_list = result[offset_start:offset_end]
            pages = (len(result) - 1) / app.config['PER_PAGE'] + 1
            if pages <= 0:
                pages = 1
            info = {'info_list': return_list, 'pages': pages, 'searched': 'ok'}
            response = flask.Response(json.dumps(info))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        except:
            info = {'searched': 'failed'}
            response = flask.Response(json.dumps(info))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200


@app.route('/medical-case-of-illness/step-info', methods=['GET'])
def get_step_info():
    case_id = request.args['case_id']
    illness_case = Illness_case.query.filter_by(case_id=case_id).first()
    if illness_case:
        step_string = illness_case.step
        tooth_step_list = step_string.split(',')
        if '' in tooth_step_list:
            tooth_step_list.remove('')
        num_list = []
        for i in range(len(tooth_step_list)):
            num_list.append((int)(tooth_step_list[i]))
        response = flask.Response(json.dumps(num_list))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 200
    else:
        response = flask.Response('can not find this case')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 403


@app.route('/medical-case-of-illness/all-user', methods=['GET'])
def get_all_user():
    user_list = User.query.all()
    user_response_list = []
    for user in user_list:
        diagnose_list = _get_user_diagnose(user.user_id)
        dit = user.get_dict()
        dit['diagnose_list'] = diagnose_list
        dit['age'] = calculate_age(user.id_number)
        user_response_list.append(dit)
    response = flask.Response(json.dumps(user_response_list))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200

@app.route('/medical-case-of-illness/user-tooth-info',methods=['GET'])
def get_user_tooth_info():
    user_id = request.args['user_id']
    tooth_list = Tooth_location.query.filter_by(user_id = user_id).all()
    response_info = []
    for tooth in tooth_list:
        case_list = Illness_case.query.filter_by(tooth_id = tooth.tooth_id).all()
        case_info_list = []
        for case in case_list:
            step_string = case.step
            tooth_step_list = step_string.split(',')
            if '' in tooth_step_list:
                tooth_step_list.remove('')
            num_list = []
            for i in range(len(tooth_step_list)):
                num_list.append((int)(tooth_step_list[i]))
            case_info = {}
            case_info['case_id'] = case.case_id
            case_info['step']=num_list
            case_info['judge_doctor']=case.judge_doctor
            case_info['if_handle'] = case.if_handle
            case_info['case_type'] = case.case_type
            case_info_list.append(case_info)
        response_info.append(case_info_list)
    response = flask.Response(json.dumps(response_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200


@app.route('/medical-case-of-illness/other-info', methods=['GET'])
def get_other_info():
    user_id = request.args['user_id']
    user = User.query.filter_by(user_id=user_id).all()
    if user:
        lit = []
        risk = Risk_assessment.query.filter_by(user_id=user_id).all()
        if risk:
            lit.append('risk')
        personal_history = Personal_history.query.filter_by(user_id=user_id).all()
        if personal_history:
            lit.append('personal_history')
        prognosis_of_management = Prognosis_of_management.query.filter_by(user_id=user_id).all()
        if prognosis_of_management:
            lit.append('prognosis_of_management')
        response = flask.Response(json.dumps(lit))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 200
    else:
        response = flask.Response('can not find this user')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 403


def _get_user_diagnose(user_id):
    tooth_list = Tooth_location.query.filter_by(user_id=user_id).all()
    diagnose_list = []
    for tooth in tooth_list:
        case_list = Tooth_location.query.filter_by(tooth_id=tooth.tooth_id).all()
        tooth_number = case_list[-1].tooth_location_number
        diagnose = Diagnose.query.filter_by(tooth_id=tooth.tooth_id).all()
        diagnose_str = ''
        if diagnose:
            diagnose_str = diagnose[-1].caries_degree
        diagnose_list.append((str(tooth_number)) + diagnose_str)
    return_str = ''
    for item in diagnose_list:
        return_str += item
        return_str +=','
    return return_str


def _search_special(key):
    return_list = []
    if key == 'consciously_reduce_salivary_flow':
        return_list = db.session.query(Personal_history).filter(and_(
            Personal_history.consciously_reduce_salivary_flow != None,
            Personal_history.consciously_reduce_salivary_flow != '')).all()
    elif key == 'salivary_gland_disease':
        return_list = db.session.query(Personal_history).filter(and_(
            Personal_history.salivary_gland_disease != None, Personal_history.salivary_gland_disease != '')).all()
    return return_list
