import httplib
import json
import flask
from flask import request
from src import app
from src.entity.oral_examination import Oral_examination
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db
from src.entity.tooth_location import Tooth_location


@app.route('/medical-case-of-illness/oral-examination', methods=['POST', 'PUT', 'GET','OPTIONS'])
def add_new_oral_examination():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            oral_examination = _form_to_oral_examination(request.form)
            db.session.add(oral_examination)
            db.session.commit()
            db.session.query(Tooth_location).filter(
                Tooth_location.tooth_id == (int)(oral_examination.tooth_id)).update(
                {'tooth_location_number': oral_examination.tooth_location})
            db.session.query(Oral_examination).filter(
                Oral_examination.tooth_id == (int)(oral_examination.tooth_id)).update(
                {'tooth_location': oral_examination.tooth_location})
            oral_examination = Oral_examination.query.filter_by(user_id=request.form['user_id']).all()[-1]
            refresh_step(oral_examination.case_id, 2)
            oral_examination_list = Oral_examination.query.filter_by(user_id=request.form['user_id']).all()
            response = oral_examination_list[-1]
            response = response.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'PUT':
        if check_if_user_exist(request.form['user_id']):
            db.session.query(Oral_examination).filter(Oral_examination.case_id == request.form['case_id']).delete()
            db.session.commit()
            oral_examination = _form_to_oral_examination(request.form)
            db.session.add(oral_examination)
            db.session.commit()
            res_oral_examination = Oral_examination.query.filter_by(case_id=request.form['case_id']).first()
            response = res_oral_examination.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'GET':
        id = request.args['case_id']
        res_oral_examination = Oral_examination.query.filter_by(case_id=id).first()
        if res_oral_examination:
            response = flask.Response(json.dumps(res_oral_examination.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        else:
            response = flask.Response("Can not find the oral examination...")
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret


def _form_to_oral_examination(form):
    temp_oral_examination = Oral_examination()
    temp_oral_examination.tooth_id = form['tooth_id']
    temp_oral_examination.case_id = form['case_id']
    temp_oral_examination.user_id = form['user_id']
    temp_oral_examination.tooth_location = form['tooth_location']
    temp_oral_examination.tooth_type = form['tooth_type']
    temp_oral_examination.caries_tired = form['caries_tired']
    temp_oral_examination.depth = form['depth']
    temp_oral_examination.fill = form['fill']
    temp_oral_examination.secondary = form['secondary']
    temp_oral_examination.color_of_caries = form['color_of_caries']
    temp_oral_examination.flex_of_caries = form['flex_of_caries']
    temp_oral_examination.cold = form['cold']
    temp_oral_examination.hot = form['hot']
    temp_oral_examination.touch = form['touch']
    temp_oral_examination.bite = form['bite']
    temp_oral_examination.vitality_value_of_teeth = form['vitality_value_of_teeth']
    temp_oral_examination.gingival_hyperemia = form['gingival_hyperemia']
    temp_oral_examination.gingival_color = form['gingival_color']
    temp_oral_examination.bop = form['bop']
    temp_oral_examination.tartar_down = form['tartar_down']
    temp_oral_examination.tartar_up = form['tartar_up']
    temp_oral_examination.periodontal_pocket_depth = form['periodontal_pocket_depth']
    temp_oral_examination.furcation = form['furcation']
    temp_oral_examination.location = form['location']
    temp_oral_examination.fistula = form['fistula']
    temp_oral_examination.overflow_pus = form['overflow_pus']
    temp_oral_examination.mobility = form['mobility']
    temp_oral_examination.relations_between_teeth = form['relations_between_teeth']
    temp_oral_examination.is_teeth_crowd = form['is_teeth_crowd']
    temp_oral_examination.involution_teeth = form['involution_teeth']
    temp_oral_examination.tooth_shape = form['tooth_shape']
    temp_oral_examination.X_Ray_location = form['X_Ray_location']
    temp_oral_examination.X_Ray_depth = form['X_Ray_depth']
    temp_oral_examination.X_Ray_fill_quality = form['X_Ray_fill_quality']
    temp_oral_examination.CT_shows = form['CT_shows']
    temp_oral_examination.piece = form['piece']
    return temp_oral_examination