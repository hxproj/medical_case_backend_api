import httplib
import json

import datetime
import flask
from flask import request
from src import app
from src.controller.common_function import check_if_user_exist, refresh_step
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
                db.session.add(risk)
                db.session.commit()
                refresh_step(request.form['case_id'], 3)
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



def _form_to_risk(form):
    risk = Risk_assessment()
    risk.tooth_id = form['tooth_id']
    risk.case_id = form['case_id']
    risk.user_id = form['user_id']
    risk.early_carie = form['early_carie']
    risk.can_see = form['can_see']
    risk.lost_tooth = form['lost_tooth']
    risk.system_illness = form['system_illness']
    risk.illness_name = form['illness_name']
    risk.times_of_carbohydrate = form['times_of_carbohydrate']
    risk.consumption_of_carbohydrate = form['consumption_of_carbohydrate']
    risk.times_of_meal = form['times_of_meal']
    risk.speed_of_saliva = form['speed_of_saliva']
    risk.ablity_saliva = form['ablity_saliva']
    risk.bacteria = form['bacteria']
    risk.consumption = form['consumption']
    risk.fluorine_with_water = form['fluorine_with_water']
    risk.fluorine = form['fluorine']
    risk.seal = form['seal']
    risk.times_of_tooth_brush = form['times_of_tooth_brush']
    risk.long_of_tooth_brush = form['long_of_tooth_brush']
    risk.health_care = form['health_care']
    return risk