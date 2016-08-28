import httplib
import json
import flask
from flask import request
from src import app
from src.entity.illness_history import Illness_history
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db

@app.route('/medical-case-of-illness/illness-history',methods=['POST','PUT','GET'])
def add_new_illness_history():
    if request.method=='POST':
        if check_if_user_exist(request.form['user_id']):
            illness_history = _form_to_illness_history(request.form)
            db.session.add(illness_history)
            db.session.commit()
            refresh_step(request.form['tooth_id'],1)
            illness_history_list = Illness_history.query.filter_by(user_id = request.form['user_id']) #todo add try except
            current_illness_history = illness_history_list[-1]
            response = current_illness_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method=='PUT':
        if check_if_user_exist(request.form['user_id']):
            illness_history = _form_to_illness_history(request.form)
            db.session.query(Illness_history).filter(Illness_history.tooth_id == request.form['tooth_id']).delete()
            db.session.commit()
            db.session.add(illness_history)
            db.session.commit()
            res_illness_history = Illness_history.query.filter_by(tooth_id = request.form['tooth_id']).first()
            response = res_illness_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method=='GET':
        id = request.args['tooth_id']
        illness_history = Illness_history.query.filter_by(tooth_id = id).first()
        response = illness_history.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret

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
    temp_history.fill_type = form['fill_type']
    return temp_history