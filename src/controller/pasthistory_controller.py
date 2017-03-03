import httplib
import json
import flask
from flask import request
from src import app
from src.entity.past_history import PastHistory
from src.controller.common_function import check_if_user_exist
from src import db


@app.route('/medical-case-of-illness/past-history', methods=['POST', 'PUT', 'GET', 'OPTIONS'])
def add_new_past_history():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            past_history = _form_to_past_history(request.form)
            db.session.add(past_history)
            db.session.commit()
            response_history = PastHistory.query.filter_by(case_id=request.form['case_id']).first()
            response = response_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'PUT':
        if check_if_user_exist(request.form['user_id']):
            past_history = _form_to_past_history(request.form)
            db.session.query(PastHistory).filter(PastHistory.case_id == request.form['case_id']).delete()
            db.session.commit()
            db.session.add(past_history)
            db.session.commit()
            res_past_history = PastHistory.query.filter_by(case_id=request.form['case_id']).first()
            response = res_past_history.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'GET':
        illness_history = PastHistory.query.filter_by(case_id=request.args['case_id']).first()
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


def _form_to_past_history(form):
    temp_history = PastHistory()
    temp_history.case_id = form['case_id']
    temp_history.tooth_id = form['tooth_id']
    temp_history.user_id = form['user_id']
    temp_history.systemillness = form['systemillness']
    temp_history.infectiousdisease = form['infectiousdisease']
    temp_history.dragallergy = form['dragallergy']

    return temp_history
