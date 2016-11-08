import httplib
import json
import flask
from flask import request
from src import app
from src.entity.illness_history import Illness_history
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db


@app.route('/medical-case-of-illness/illness-history', methods=['POST', 'PUT', 'GET', 'OPTIONS'])
def add_new_illness_history():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            illness_history = _form_to_illness_history(request.form)
            db.session.add(illness_history)
            db.session.commit()
            temp_illness = Illness_history.query.filter_by(user_id=request.form['user_id']).all()[-1]
            refresh_step(temp_illness.tooth_id, 1)
            illness_history_list = Illness_history.query.filter_by(
                user_id=request.form['user_id'])  # todo add try except
            current_illness_history = illness_history_list[-1]
            response = current_illness_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'PUT':
        if check_if_user_exist(request.form['user_id']):
            illness_history = _form_to_illness_history(request.form)
            db.session.query(Illness_history).filter(Illness_history.tooth_id == request.form['tooth_id']).delete()
            db.session.commit()
            db.session.add(illness_history)
            db.session.commit()
            res_illness_history = Illness_history.query.filter_by(tooth_id=request.form['tooth_id']).first()
            response = res_illness_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'GET':
        id = request.args['tooth_id']
        illness_history = Illness_history.query.filter_by(tooth_id=id).first()
        if illness_history:
            response = flask.Response(json.dumps(illness_history.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        else:
            response = flask.Response("Can not find the illness history...")
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret


def _form_to_illness_history(form):
    temp_history = Illness_history()
    temp_history.tooth_id = form['tooth_id']
    temp_history.user_id = form['user_id']
    temp_history.is_night_pain_self_pain = form['is_night_pain_self_pain']
    temp_history.is_primary = form['is_primary']
    temp_history.is_very_bad = form['is_very_bad']
    temp_history.is_relief = form['is_relief']
    temp_history.medicine_name = form['medicine_name']
    temp_history.fill_type = form['fill_type']
    temp_history.is_hypnalgia = form['is_hypnalgia']
    temp_history.is_sensitive_cold_heat = form['is_sensitive_cold_heat']
    temp_history.is_cold_hot_stimulationpain = form['is_cold_hot_stimulationpain']
    temp_history.is_delayed_pain = form['is_delayed_pain']
    temp_history.cure_time = form['cure_time']
    temp_history.fill_state = form['fill_state']

    return temp_history
