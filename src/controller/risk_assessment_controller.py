import copy
import httplib
import json

import datetime
import flask
from flask import request
from src import app
from src.controller.common_function import check_if_user_exist, refresh_step
from src.entity.prognosis_of_management import Prognosis_of_management
from src.entity.risk_assessment import Risk_assessment
from src import db

@app.route('/medical-case-of-illness/risk-assessment',methods=['GET','POST','PUT','DELETE','OPTIONS'])
def risk_options():
    if request.method=='POST':
        if not check_if_user_exist(request.form['user_id']):
            response = flask.Response('user is not exist .')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response ,400
        else:
            if not Risk_assessment.query.filter_by(case_id = request.form['case_id']).first():
                risk = _form_to_risk(request.form)
                risk.risk_level = _get_risk_level(risk)
                prognosis_of_management = Prognosis_of_management()
                prognosis_of_management.user_id = risk.user_id
                prognosis_of_management.case_id = risk.case_id
                prognosis_of_management.tooth_id = risk.tooth_id
                prognosis_of_management.patient_type = risk.risk_level
                db.session.query(Prognosis_of_management).filter(Prognosis_of_management.case_id == risk.case_id).delete()
                db.session.add(prognosis_of_management)
                db.session.add(risk)
                db.session.commit()
                refresh_step(request.form['case_id'], 3)
                #refresh_step(request.form['case_id'], 7)
                response = flask.Response(json.dumps(Risk_assessment.query.filter_by(case_id=request.form['case_id']).first().get_dict()))
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response, 200
            else:
                response = flask.Response('this risk record is already exist ')
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response, 400
    elif request.method =='GET':
        risk = Risk_assessment.query.filter_by(case_id = request.args['case_id']).first()
        if risk:
            response = flask.Response(json.dumps(risk.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        else:
            response = flask.Response('user has not record risk assessment.')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method=='DELETE':
        risk = Risk_assessment.query.filter_by(case_id=request.args['case_id']).first()
        if risk:
            db.session.query(Risk_assessment).filter(Risk_assessment.case_id==request.args['case_id']).delete()
            db.session.commit()
            response = flask.Response('succeed')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        else:
            response = flask.Response('user has not record risk assessment.')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'PUT':
        if not check_if_user_exist(request.form['user_id']):
            response = flask.Response('user is not exist .')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
        else:
            if Risk_assessment.query.filter_by(case_id=request.form['case_id']).first():
                db.session.query(Risk_assessment).filter(Risk_assessment.case_id==request.form['case_id']).delete()
                db.session.commit()
                risk = _form_to_risk(request.form)
                risk.risk_level = _get_risk_level(risk)
                prognosis_of_management = Prognosis_of_management()
                prognosis_of_management.user_id = risk.user_id
                prognosis_of_management.case_id = risk.case_id
                prognosis_of_management.tooth_id = risk.tooth_id
                prognosis_of_management.patient_type = risk.risk_level
                db.session.query(Prognosis_of_management).filter(
                    Prognosis_of_management.case_id == risk.case_id).delete()
                db.session.add(prognosis_of_management)
                db.session.add(risk)
                db.session.commit()
                response = flask.Response(
                    json.dumps(Risk_assessment.query.filter_by(case_id=request.form['case_id']).first().get_dict()))
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response, 200
            else:
                response = flask.Response('this risk record is not already exist ')
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response, 400
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret

def _get_risk_level(risk):
    level = 1
    result_lit = []
    json_data = _get_json_data()
    copy_risk = copy.deepcopy(risk)
    risk_dit = copy_risk.get_dict()
    for key,value in risk_dit.items():
        if json_data.has_key(key):
            for match in json_data[key]:
                if match['key'] == value:
                    result_lit.append(match['value'])
                    break
    result_set = set(result_lit)
    if 3 in result_set:
        level = 3
    elif 3 not in result_set and 2 in result_set:
        level = 2
    else:
        level =1
    return level

def _get_json_data():
    with open('./templete/risk.json') as json_file:
        data = json.load(json_file)
        return data

def _form_to_risk(form):
    risk = Risk_assessment()
    risk.tooth_id = form['tooth_id']
    risk.case_id = form['case_id']
    risk.user_id = form['user_id']
    risk.fluorine_protection = form['fluorine_protection']
    risk.sugary_foods = form['sugary_foods']
    risk.relative_illness = form['relative_illness']
    risk.need_record = form['need_record']
    risk.alcohol_drugs = form['alcohol_drugs']
    risk.radiotherapy = form['radiotherapy']
    risk.eating_disorders = form['eating_disorders']
    risk.saliva_medicine = form['saliva_medicine']
    risk.special_care = form['special_care']
    risk.caries_lost = form['caries_lost']
    risk.soft_dirt = form['soft_dirt']
    risk.special_tooth_shape = form['special_tooth_shape']
    risk.adjacent_caries = form['adjacent_caries']
    risk.tooth_exposure = form['tooth_exposure']
    risk.fill_overhang = form['fill_overhang']
    risk.appliance = form['appliance']
    risk.dry_syndrome = form['dry_syndrome']
    risk.hole = form['hole']
    return risk