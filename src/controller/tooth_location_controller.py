import httplib
import json

import datetime
import flask
from flask import request
from src import app
from src.entity.illness_case import Illness_case
from src.entity.tooth_location import Tooth_location
from src.entity.illness_history import Illness_history
from src.entity.oral_examination import Oral_examination
from src.entity.difficulty_assessment import Difficulty_assessment
from src.entity.surgical import Surgical
from src.entity.diagnose import Diagnose
from src.entity.non_surgical import Non_surgical
from src.entity.user import User
from src.entity.usphs import Usphs
from src.controller.common_function import check_if_user_exist, refresh_step, delete_directory
from src import db


@app.route('/medical-case-of-illness/tooth-location-record', methods=['GET','POST', 'PUT', 'DELETE','OPTIONS'])
def add_new_tooth_location_record():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            location_record = _form_to_tooth_location_record(request.form)
            doctor = request.form['judge_doctor']
            #location_record.step = 0
            db.session.add(location_record)
            db.session.commit()
            #refresh_step(request.form['user_id'], 0, request.form['tooth_location'])
            response_record = Tooth_location.query.filter_by(user_id=request.form['user_id']).all()
            newest_record = response_record[-1]
            illness_case = Illness_case()
            illness_case.tooth_id = newest_record.tooth_id
            illness_case.date = datetime.datetime.now()
            illness_case.case_type=0
            illness_case.step = '0,'
            illness_case.if_handle = 1
            illness_case.judge_doctor = doctor
            db.session.add(illness_case)
            db.session.commit()
            newest_case = Illness_case.query.filter_by(tooth_id = newest_record.tooth_id).all()[-1]
            response = newest_record.get_dict()
            response['case_id']=newest_case.case_id
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'GET':
        tooth_id = request.args['tooth_id']
        tooth_location = Tooth_location.query.filter_by(tooth_id = tooth_id).first()
        if tooth_location:
            response = tooth_location.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret,200
        else:
            res = flask.Response('can not find this record')
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res,400

    elif request.method == 'PUT':
        Tooth_location.query.filter_by(tooth_id=request.form['tooth_id']).update({'is_fill_tooth':request.form['is_fill_tooth'],
                                                                                  'symptom':request.form['symptom'],'time_of_occurrence'
                                                                                  :request.form['time_of_occurrence'],'tooth_location'
                                                                                  :request.form['tooth_location'],'additional':request.form['additional']})
        db.session.commit()
        response_record = Tooth_location.query.filter_by(tooth_id=request.form['tooth_id']).first()
        response = response_record.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'DELETE':
        tooth_id = request.args.get('tooth_id')
        deletelist = db.session.query(Tooth_location).filter(Tooth_location.tooth_id == tooth_id).first()
        # step = deletelist.step
        count = 0
        if db.session.query(Tooth_location).filter(Tooth_location.tooth_id == tooth_id).delete():
            count = count + 1
        if db.session.query(Illness_history).filter(Illness_history.tooth_id == tooth_id).delete():
            count = count + 1
        if db.session.query(Oral_examination).filter(Oral_examination.tooth_id == tooth_id).delete():
            count = count + 1
        if db.session.query(Diagnose).filter(Diagnose.tooth_id == tooth_id).delete():
            count = count + 1
        if db.session.query(Difficulty_assessment).filter(Difficulty_assessment.tooth_id == tooth_id).delete():
            count = count + 1
        if db.session.query(Surgical).filter(Surgical.tooth_id == tooth_id).delete():
            count = count + 1
        if db.session.query(Non_surgical).filter(Non_surgical.tooth_id == tooth_id).delete():
            count = count + 1
        if db.session.query(Usphs).filter(Usphs.tooth_id == tooth_id).delete():
            count = count + 1
        db.session.commit()
        case_list = Illness_case.query.filter_by(tooth_id=tooth_id).all()
        for case in case_list:
            delete_directory(case.case_id) # todo : delete all case directory ? done
        ret = flask.Response("Delete Successful")
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret


def _form_to_tooth_location_record(form):
    temp_record = Tooth_location()
    temp_record.tooth_location_number = form['tooth_location_number']
    #temp_record.symptom = form['symptom']
    temp_record.user_id = form['user_id']
    #temp_record.time_of_occurrence = form['time_of_occurrence']
    #temp_record.is_fill_tooth = form['is_fill_tooth']
    #temp_record.step = '0,'
    return temp_record


def _form_to_tooth_location_record_update(form):
    temp_record = _form_to_tooth_location_record(form)
    temp_record.tooth_id = form['tooth_id']
    return temp_record
