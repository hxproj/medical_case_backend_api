import httplib
import json
import flask
from flask import request
from src import app
from src.entity.illness_history import Illness_history
from src.controller.common_function import check_if_user_exist
from src import db

@app.route('/medical-case-of-illness/illness-history',methods=['POST'])
def add_new_illness_history():
    if check_if_user_exist(request.form['user_id']):
        illness_history = _form_to_illness_history(request.form)
        db.session.add(illness_history)
        db.session.commit()
        illness_history_list = Illness_history.query.filter_by(user_id = request.form['user_id']) #todo add try except
        current_illness_history = illness_history_list[-1]
        response = current_illness_history.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    else:
        ret = flask.Response("Can't find this user")
        return ret, httplib.BAD_REQUEST


def _form_to_illness_history(form):
    temp_history =Illness_history()
    temp_history.tooth_id = form['tooth_id']
    temp_history.is_medicine = form['is_medicine']
    temp_history.is_night_pain_self_pain = form['is_night_pain_self_pain']
    temp_history.user_id = form['user_id']
    temp_history.is_primary = form['is_primary']
    temp_history.is_very_bad = form['is_very_bad']
    temp_history.is_relief = form['is_relief']
    temp_history.is_treatment = form['is_treatment']
    temp_history.medicine_name = form['medicine_name']
    return temp_history