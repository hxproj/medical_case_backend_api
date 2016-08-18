import httplib
import json

import flask
from flask import request
from src import app
from src.entity.tooth_location import Tooth_location
from src.controller.common_function import check_if_user_exist
from src import db

@app.route('/medical-case-of-illness/tooth-location-record',methods=['POST'])
def add_new_tooth_location_record():
    if check_if_user_exist(request.form['user_id']):
        location_record = _form_to_tooth_location_record(request.form)
        db.session.add(location_record)
        db.session.commit()
        response_record = Tooth_location.query.filter_by(user_id = request.form['user_id']).all()
        newest_record = response_record[-1]
        response = newest_record.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    else:
        ret = flask.Response("Can't find this user")
        return ret, httplib.BAD_REQUEST


def _form_to_tooth_location_record(form):
    temp_record =Tooth_location()
    temp_record.tooth_location = form['tooth_location']
    temp_record.symptom = form['symptom']
    temp_record.user_id = form['user_id']
    temp_record.time_of_occurrence = form['time_of_occurrence']
    temp_record.is_fill_tooth = form['is_fill_tooth']
    return temp_record