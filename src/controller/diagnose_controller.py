import httplib
import json
import flask
from flask import request
from src import app
from src.entity.diagnose import Diagnose
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db


@app.route('/medical-case-of-illness/diagnose', methods=['POST', 'PUT', 'GET', 'OPTIONS'])
def add_new_diagnose():
    if request.method == 'GET':
        diagnose = Diagnose.query.filter_by(case_id=request.args['case_id']).first()
        if diagnose:
            response = flask.Response(json.dumps(diagnose.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        else:
            response = flask.Response("Can not find the diagnose...")
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            diagnose = _form_to_diagnose(request.form)
            db.session.add(diagnose)
            db.session.commit()
            diagnose = Diagnose.query.filter_by(user_id=request.form['user_id']).all()[-1]
            refresh_step(diagnose.case_id, 4)
            diagnose_ret = Diagnose.query.filter_by(case_id=request.form['case_id']).first()
            response = diagnose_ret.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'PUT':
        if check_if_user_exist(request.form['user_id']):
            diagnose = _form_to_diagnose(request.form)
            db.session.query(Diagnose).filter(
                Diagnose.case_id == request.form['case_id']).delete()
            db.session.commit()
            db.session.add(diagnose)
            db.session.commit()
            res_diagnose = Diagnose.query.filter_by(case_id=request.form['case_id']).first()
            response = res_diagnose.get_dict()
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


def _form_to_diagnose(form):
    temp_diagnose = Diagnose()
    temp_diagnose.caries_degree = form['caries_degree']
    temp_diagnose.case_id = form['case_id']
    temp_diagnose.tooth_id = form['tooth_id']
    temp_diagnose.user_id = form['user_id']
    temp_diagnose.caries_type = form['caries_type']
    temp_diagnose.caries_type = form['cure_plan']
    temp_diagnose.caries_type = form['specification']
    temp_diagnose.caries_type = form['if_direct']

    return temp_diagnose
