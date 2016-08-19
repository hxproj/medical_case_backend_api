import httplib
import json
import flask
from flask import request
from src import app
from src.entity.difficulty_assessment import Difficulty_assessment
from src.controller.common_function import check_if_user_exist
from src import db

@app.route('/medical-case-of-illness/difficulty-assessment',methods=['POST','PUT'])
def add_new_difficulty_assessment():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            ret_difficult = _form_to_difficult_assessment(request.form)
            db.session.add(ret_difficult)
            db.session.commit()
            res_difficult = Difficulty_assessment.query.filter_by(tooth_id=request.form['tooth_id']).first()
            response = res_difficult.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'PUT':
        if check_if_user_exist(request.form['user_id']):
            ret_difficult = _form_to_difficult_assessment(request.form)
            db.session.query(Difficulty_assessment).filter(Difficulty_assessment.tooth_id == request.form['tooth_id']).delete()
            db.session.commit()
            db.session.add(ret_difficult)
            db.session.commit()
            res_difficulty_assessment =Difficulty_assessment.query.filter_by(tooth_id = request.form['tooth_id']).first()
            response = res_difficulty_assessment.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST

def _form_to_difficult_assessment(form):
    temp_difficult = Difficulty_assessment()
    temp_difficult.tooth_id = form['tooth_id']
    temp_difficult.user_id = form['user_id']
    temp_difficult.tooth_surface_and_location = form['tooth_surface_and_location']
    temp_difficult.caries_depth = form['caries_depth']
    temp_difficult.technology_type = form['technology_type']
    temp_difficult.history_of_fill = form['history_of_fill']
    temp_difficult.mouth_opening = form['mouth_opening']
    temp_difficult.gag_reflex = form['gag_reflex']
    temp_difficult.saliva = form['saliva']
    temp_difficult.dental_phobia = form['dental_phobia']
    temp_difficult.difficulty_rating = form['difficulty_rating']
    return  temp_difficult