import copy
import httplib
import json

import datetime
from operator import and_

import flask
from flask import request
from sqlalchemy import func

from src import app
from src.controller.common_function import check_if_user_exist, get_user_info_list, calculate_age
from src.entity.diagnose import Diagnose
from src.entity.difficulty_assessment import Difficulty_assessment
from src.entity.illness_case import Illness_case
from src.entity.illness_history import Illness_history
from src.entity.oral_examination import Oral_examination
from src.entity.personal_history import Personal_history
from src.entity.past_history import PastHistory
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
    case_id_list = []
    for result in result_list:
        case_id_list.append(result.case_id)
    temp_set = set(case_id_list)
    case_id_list = list(temp_set)
    result_list = []
    for case_id in case_id_list :
        case = Illness_case.query.filter_by(case_id=case_id).first()
        tooth_location = ''
        if case:
            tooth_location = Tooth_location.query.filter_by(tooth_id = case.tooth_id).first()
        temp_case = copy.deepcopy(case)
        case_dict = temp_case.get_dict()
        case_dict['user_id'] = tooth_location.user_id
        result_list.append(case_dict)
    result = result_list[-1::-1]
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
    page = request.args.get('page', 1, type=int)
    order_by = request.args.get('order', 'user_id')
    order_type = request.args.get('order_type', 1, type=int)
    offset = (page - 1) * app.config['PER_PAGE']
    specific_value = request.args.get('value')
    pre_value = request.args.get('pre_value')
    post_value = request.args.get('post_value')
    parameter = request.args.get('parameter')
    pre_query = ''
    if parameter and parameter != '':
        if specific_value and specific_value != '':
            if parameter == "user_id":
                pre_query = db.session.query(User).filter(User.user_id == specific_value)
            elif parameter == "in_date":
                pre_query = db.session.query(User).filter(User.in_date.like('%'+specific_value+'%'))
            elif parameter == "name":
                pre_query = db.session.query(User).filter(User.name == specific_value)
            elif parameter == "age":
                date_now = datetime.datetime.now()
                current_date_num = date_now.year * 10000 + date_now.month*100 + date_now.day
                pre_age = current_date_num - int(specific_value) * 10000
                post_age = current_date_num - (int(specific_value) + 1) * 10000
                pre_query = db.session.query(User).filter(and_(User.birthday > post_age,User.birthday<pre_age))
        elif pre_value and post_value:
            if parameter == "user_id":
                pre_query = db.session.query(User).filter(and_(User.user_id > pre_value, User.user_id < post_value))
            elif parameter == "in_date":
                pre_query = db.session.query(User).filter(and_(User.in_date > str(pre_value), User.in_date < str(post_value)))
            elif parameter == "name":
                pre_query = db.session.query(User).filter(and_(User.name > pre_value, User.name < post_value))
            elif parameter == "age":
                date_now = datetime.datetime.now()
                current_date_num = date_now.year * 10000 + date_now.month * 100 + date_now.day
                pre_age = current_date_num - int(post_value) * 10000
                post_age = current_date_num - (int(pre_value) - 1) * 10000
                pre_query = db.session.query(User).filter(and_(User.birthday > pre_age, User.birthday < post_age))
    else:
        pre_query = db.session.query(User)
    query = ""
    if order_type == 1:
        if order_by == "user_id":
            query = pre_query.order_by(User.user_id)
        elif order_by == "in_date":
            query = pre_query.order_by(User.in_date)
        elif order_by == "name":
            query = pre_query.order_by(User.name)
        elif order_by == "age":
            query = pre_query.order_by(User.birthday)
    elif order_type == 2:
        if order_by == "user_id":
            query = pre_query.order_by(User.user_id.desc())
        elif order_by == "in_date":
            query = pre_query.order_by(User.in_date.desc())
        elif order_by == "name":
            query = pre_query.order_by(User.name.desc())
        elif order_by == "age":
            query = pre_query.order_by(User.birthday.desc())
    query = query.offset(offset)
    query = query.limit(app.config['PER_PAGE'])
    user_list = query.all()
    user_response_list = []
    for user in user_list:
        diagnose_list = _get_user_diagnose(user.user_id)
        dit = user.get_dict()
        dit['diagnose_list'] = diagnose_list
        dit['age'] = calculate_age(user.id_number)
        user_response_list.append(dit)
    count = db.session.query(func.count(User.user_id)).all()[0][0]
    count = count / app.config['PER_PAGE'] + 1
    response_dict = {"pages": count, "user_list": user_response_list}
    response = flask.Response(json.dumps(response_dict))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200


@app.route('/medical-case-of-illness/user-all-tooth-info', methods=['GET'])
def get_user_all_tooth_info():
    user_id = request.args['user_id']
    tooth_list = Tooth_location.query.filter_by(user_id=user_id).all()
    response_info = []
    for tooth in tooth_list:
        case_list = Illness_case.query.filter_by(tooth_id=tooth.tooth_id).all()
        tooth_info = {}
        case_info_list = []
        for case in case_list:
            step_string = case.step
            tooth_step_list = step_string.split(',')
            if '' in tooth_step_list:
                tooth_step_list.remove('')
            num_list = []
            for i in range(len(tooth_step_list)):
                num_list.append(int(tooth_step_list[i]))
            case_info = {}
            case_info['case_id'] = case.case_id
            case_info['step'] = num_list
            case_info['judge_doctor'] = case.judge_doctor
            case_info['if_handle'] = case.if_handle
            case_info['case_type'] = case.case_type
            case_info['date'] = case.date.strftime('%Y-%m-%d %H:%M')
            case_info_list.append(case_info)
        tooth_info['tooth_id'] = tooth.tooth_id
        tooth_info['tooth_location_number'] = tooth.tooth_location_number
        tooth_info['cases'] = case_info_list
        response_info.append(tooth_info)
    response = flask.Response(json.dumps(response_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200


@app.route('/medical-case-of-illness/user-tooth-info', methods=['GET'])
def get_user_tooth_info():
    this_tooth_id = request.args['tooth_id']
    case_info_list = []

    case_list = Illness_case.query.filter_by(tooth_id=this_tooth_id).all()
    for case in case_list:
        step_string = case.step
        tooth_step_list = step_string.split(',')
        if '' in tooth_step_list:
            tooth_step_list.remove('')
        num_list = []
        for i in range(len(tooth_step_list)):
            num_list.append(int(tooth_step_list[i]))
        case_info = {}
        case_info['case_id'] = case.case_id
        case_info['step'] = num_list
        case_info['judge_doctor'] = case.judge_doctor
        case_info['if_handle'] = case.if_handle
        case_info['case_type'] = case.case_type
        case_info['date'] = case.date.strftime('%Y-%m-%d %H:%M')
        case_info_list.append(case_info)

    tooth_info = {}
    this_tooth_info = Tooth_location.query.filter_by(tooth_id=this_tooth_id).first()
    if this_tooth_info:
        tooth_info['tooth_id'] = this_tooth_info.tooth_id
        tooth_info['tooth_location_number'] = this_tooth_info.tooth_location_number
        tooth_info['cases'] = case_info_list

    response = flask.Response(json.dumps(tooth_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200


@app.route('/medical-case-of-illness/self-say-history', methods=['GET'])
def get_self_say_and_history():
    case_id = request.args['case_id']
    personal_history = Personal_history.query.filter_by(case_id=case_id).first()
    illness_history = Illness_history.query.filter_by(case_id=case_id).first()
    past_history = PastHistory.query.filter_by(case_id=case_id).first()
    tooth_location = ''
    if illness_history:
        tooth_location = Tooth_location.query.filter_by(tooth_id=illness_history.tooth_id).first()
    response_dit = {}
    if tooth_location and illness_history and personal_history:
        response_dit['chief_complaint'] = dict(tooth_location.get_dict().items())
        response_dit['personal_history'] = dict(personal_history.get_dict().items())
        response_dit['illness_history'] = dict(illness_history.get_dict().items())
        response_dit['past_history'] = dict(past_history.get_dict().items())
        response = flask.Response(json.dumps(response_dit))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 200
    else:
        return "data error", 403


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
        diagnose_list.append(tooth_number + diagnose_str)
    return_str = ''
    for item in diagnose_list:
        return_str += item
        return_str += ', '
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
