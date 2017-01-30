import httplib
import json

import flask
from flask import request
from src import app
from src.controller.common_function import check_if_user_exist, refresh_step
from src.entity.personal_history import Personal_history
from src import db


@app.route('/medical-case-of-illness/personal-history', methods=['POST', 'PUT', 'GET', 'OPTIONS'])
def add_personal_history():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            personal_history = _form_to_personal_history(request.form)
            db.session.add(personal_history)
            db.session.commit()
            refresh_step(request.form['case_id'], 1)
            response_history = Personal_history.query.filter_by(case_id=request.form['case_id']).first()
            response = response_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret,httplib.BAD_REQUEST
    elif request.method == 'GET':
        case_id = request.args['case_id']
        personal_history = Personal_history.query.filter_by(case_id = case_id).first()
        if personal_history:
            response = flask.Response(json.dumps(personal_history.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response,200
        else:
            response = flask.Response('can not find this record.')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'PUT':
        if check_if_user_exist(request.form['user_id']):
            db.session.query(Personal_history).filter(Personal_history.case_id == request.form['case_id']).delete()
            db.session.commit()
            personal_history = _form_to_personal_history(request.form)
            db.session.add(personal_history)
            db.session.commit()
            response_history = Personal_history.query.filter_by(case_id=request.form['case_id']).first()
            response = response_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret


def _form_to_personal_history(form):
    history = Personal_history()
    history.user_id = form['user_id']
    history.case_id = form['case_id']
    history.tooth_id = form['tooth_id']
    history.consumption_of_sweet = form['consumption_of_sweet']
    #history.more_sweet = form['more_sweet']
    history.frequency_of_sweet = form['frequency_of_sweet']
    history.frequency_of_meal = form['frequency_of_meal']
    history.is_carbonic_acid = form['is_carbonic_acid']
    history.is_floss = form['is_floss']
    history.times_of_teeth_brush = form['times_of_teeth_brush']
    history.time_of_teeth_brush = form['time_of_teeth_brush']
    history.long_of_teeth_brush = form['long_of_teeth_brush']
    history.electric_tooth_brush = form['electric_tooth_brush']
    #history.method_of_tooth_brush = form['method_of_tooth_brush']
    history.is_fluorine = form['is_fluorine']
    history.is_cavity_examination = form['is_cavity_examination']
    history.is_periodontal_treatment = form['is_periodontal_treatment']
    history.salivary_gland_disease = form['salivary_gland_disease']
    history.sjogren_syndrome = form['sjogren_syndrome']
    if not form['consciously_reduce_salivary_flow']=='':
        history.consciously_reduce_salivary_flow = form['consciously_reduce_salivary_flow']
    else :
        history.consciously_reduce_salivary_flow=None;
    history.development_of_the_situation = form['development_of_the_situation']
    history.radiation_therapy_history = form['radiation_therapy_history']
    history.loss_caries_index_up = form['loss_caries_index_up']
    history.loss_caries_surface_index_up = form['loss_caries_surface_index_up']
    history.orthodontic = form['orthodontic']
    history.additional = form['additional']
    return history

