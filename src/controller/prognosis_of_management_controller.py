import json
import flask
from flask import request
from src import app
from src.entity.prognosis_of_management import Prognosis_of_management
from src import db


@app.route('/medical-case-of-illness/prognosis',methods=['GET','PUT','POST','OPTIONS'])
def prognosis_operation():
    if request.method=='POST':
        prognosis = Prognosis_of_management()
        prognosis.user_id = request.form['user_id']
        prognosis.patient_type=request.form['patient_type']
        db.session.add(prognosis)
        db.session.commit()
        result = Prognosis_of_management.query.filter_by(user_id = request.form['user_id']).first()
        response = result.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method=='PUT':
        prognosis = Prognosis_of_management()
        prognosis.user_id = request.form['user_id']
        prognosis.patient_type = request.form['patient_type']
        db.session.query(Prognosis_of_management).filter(
            Prognosis_of_management.user_id == request.form['user_id']).delete()
        db.session.commit()
        db.session.add(prognosis)
        db.session.commit()
        result = Prognosis_of_management.query.filter_by(user_id=request.form['user_id']).first()
        response = result.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'GET':
        prognosis = Prognosis_of_management.query.filter_by(user_id = request.args['user_id']).first()
        if prognosis:
            response = flask.Response(json.dumps(prognosis.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        else:
            response = flask.Response("Can not find the prognosis...")
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret