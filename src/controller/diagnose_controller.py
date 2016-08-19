import httplib
import json
import flask
from flask import request
from src import app
from src.entity.diagnose import Diagnose
from src.controller.common_function import check_if_user_exist
from src import db

@app.route('/medical-case-of-illness/diagnose',methods=['POST','PUT'])
def add_new_diagnose():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            diagnose = _form_to_diagnose(request.form)
            db.session.add(diagnose)
            db.session.commit()
            diagnose_ret = Diagnose.query.filter_by(tooth_id = request.form['tooth_id']).first()
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
                Diagnose.tooth_id == request.form['tooth_id']).delete()
            db.session.commit()
            db.session.add(diagnose)
            db.session.commit()
            res_diagnose = Diagnose.query.filter_by(tooth_id = request.form['tooth_id']).first()
            response = res_diagnose.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST

def _form_to_diagnose(form):
    temp_diagnose = Diagnose()
    temp_diagnose.caries_degree = form['caries_degree']
    temp_diagnose.tooth_id = form['tooth_id']
    temp_diagnose.user_id = form['user_id']
    temp_diagnose.caries_type = form['caries_type']
    return temp_diagnose