import httplib
import json

import datetime
import flask
from flask import request
from src import app
from src.entity.tooth_location import Tooth_location
from src.entity.illness_history import Illness_history
from src.entity.oral_examination import Oral_examination
from src.entity.difficulty_assessment import Difficulty_assessment
from src.entity.surgical import Surgical
from src.entity.diagnose import Diagnose
from src.entity.non_surgical import Non_surgical
from src.entity.user import User
from src.entity.usphs import Usphs
from src.entity.illness_case import Illness_case
from src.controller.common_function import check_if_user_exist, refresh_step, delete_directory
from src import db


@app.route('/medical-case-of-illness/case', methods=['GET','POST', 'PUT', 'DELETE','OPTIONS'])
def add_new_case():
    if request.method == 'POST':
        case = _form_to_case(request.form)
        user_id = Tooth_location.query.filter_by(tooth_id=request.form['tooth_id']).first().user_id
        db.session.query(User).filter_by(user_id = user_id).update(
            {User.main_doctor : request.form['judge_doctor']}
        )
        #location_record.step = 0
        db.session.add(case)
        db.session.commit()
        #refresh_step(request.form['user_id'], 0, request.form['tooth_location'])
        response_record = Illness_case.query.filter_by(tooth_id=request.form['tooth_id']).all()
        newest_record = response_record[-1]
        response = newest_record.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'GET':
        case_id = request.args['case_id']
        illness_case = Illness_case.query.filter_by(case_id = case_id).first()
        if illness_case:
            response = illness_case.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret,200
        else:
            res = flask.Response('can not find this record')
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res,400

    elif request.method == 'PUT':
        db.session.query(Illness_case).filter(Illness_case.case_id == request.form['case_id']).delete()
        user_id = Tooth_location.query.filter_by(tooth_id=request.form['tooth_id']).first().user_id
        db.session.query(User).filter_by(user_id=user_id).update(
            {User.main_doctor: request.form['judge_doctor']}
        )
        # loca
        db.session.commit()
        illness_case = _form_to_case(request.form)
        illness_case.case_id = request.form['case_id']
        db.session.add(illness_case)
        db.session.commit()
        response_record = Illness_case.query.filter_by(case_id=request.form['case_id']).first()
        response = response_record.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'DELETE':
        case_id = request.args.get('case_id')
        deletelist = db.session.query(Illness_case).filter(Illness_case.case_id == case_id).first()
        step = deletelist.step
        count = 0
        if db.session.query(Illness_case).filter(Illness_case.case_id == case_id).delete():
            count = count + 1
        if db.session.query(Illness_history).filter(Illness_history.case_id == case_id).delete():
            count = count + 1
        if db.session.query(Oral_examination).filter(Oral_examination.case_id == case_id).delete():
            count = count + 1
        if db.session.query(Diagnose).filter(Diagnose.case_id == case_id).delete():
            count = count + 1
        if db.session.query(Difficulty_assessment).filter(Difficulty_assessment.case_id == case_id).delete():
            count = count + 1
        if db.session.query(Surgical).filter(Surgical.case_id == case_id).delete():
            count = count + 1
        if db.session.query(Non_surgical).filter(Non_surgical.case_id == case_id).delete():
            count = count + 1
        if db.session.query(Usphs).filter(Usphs.case_id == case_id).delete():
            count = count + 1
        db.session.commit()
        delete_directory(case_id) # todo : delete directory by tooth_id or case id ? done
        ret = flask.Response("Delete Successful")
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret


def _form_to_case(form):
    temp_record = Illness_case()
    #temp_record.tooth_location = form['case_id']
    temp_record.tooth_id = form['tooth_id']
    temp_record.case_type = form['case_type']
    temp_record.date = datetime.datetime.now()
    temp_record.if_handle = form['if_handle']
    temp_record.judge_doctor = form['judge_doctor']
    temp_record.step = ''
    return temp_record


