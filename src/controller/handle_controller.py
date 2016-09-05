import httplib
import json
import flask
from flask import request
from src import app
from src.entity.surgical import Surgical
from src.entity.non_surgical import Non_surgical
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db


@app.route('/medical-case-of-illness/handle', methods=['POST', 'PUT','GET'])
def handle_method():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            if ((int)(request.form['handle_type']) == 0):
                non_surgical = _form_to_non_surgical(request.form)
                db.session.add(non_surgical)
                db.session.commit()
                refresh_step(request.form['tooth_id'], 5)
                ret_non_surgical = Non_surgical.query.filter_by(tooth_id=request.form['tooth_id']).first()
                response = ret_non_surgical.get_dict()
                ret = flask.Response(json.dumps(response))
                ret.headers['Access-Control-Allow-Origin'] = '*'
                return ret
            elif (int)(request.form['handle_type']) == 1:
                surgical = _form_to_surgical(request.form)
                db.session.add(surgical)
                db.session.commit()
                refresh_step(request.form['tooth_id'], 5)
                ret_surgical = Surgical.query.filter_by(tooth_id=request.form['tooth_id']).first()
                response = ret_surgical.get_dict()
                ret = flask.Response(json.dumps(response))
                ret.headers['Access-Control-Allow-Origin'] = '*'
                return ret
            else:
                ret = flask.Response('no matched opreation')
                ret.headers['Access-Control-Allow-Origin'] = '*'
                return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'GET':
        temp_result = Surgical.query.filter_by(tooth_id=request.args['tooth_id']).first()
        if temp_result:
            response = temp_result.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else :
            temp_result = Non_surgical.query.filter_by(tooth_id=request.args['tooth_id']).first()
            response = temp_result.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
    elif request.method =='PUT':
        if check_if_user_exist(request.form['user_id']):
            if (int)(request.form['handle_type'])==1:
                temp_result = _form_to_surgical(request.form)
            else:
                temp_result = _form_to_non_surgical(request.form)
            db.session.query(Surgical).filter(
                Surgical.tooth_id == request.form['tooth_id']).delete()
            db.session.query(Non_surgical).filter(
                Non_surgical.tooth_id == request.form['tooth_id']).delete()
            db.session.commit()
            db.session.add(temp_result)
            db.session.commit()
            if (int)(request.form['handle_type'])==1:
                result = Surgical.query.filter_by(tooth_id = request.form['tooth_id']).first()
            else:
                result = Non_surgical.query.filter_by(tooth_id = request.form['tooth_id']).first()
            response = result.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST


def _form_to_surgical(form):
    temp_surgical = Surgical()
    temp_surgical.user_id = form['user_id']
    temp_surgical.tooth_id = form['tooth_id']
    temp_surgical.handle_type = form['handle_type']
    temp_surgical.specific_method = form['specific_method']
    temp_surgical.anesthesia_medicine = form['anesthesia_medicine']
    temp_surgical.part_anesthesia = form['part_anesthesia']
    temp_surgical.rubber = form['rubber']
    temp_surgical.tools = form['tools']
    temp_surgical.shape_of_hole = form['shape_of_hole']
    temp_surgical.depth_of_hole = form['depth_of_hole']
    temp_surgical.is_piece = form['is_piece']
    temp_surgical.is_chock = form['is_chock']
    temp_surgical.shade_guide = form['shade_guide']
    temp_surgical.color_of_tooth = form['color_of_tooth']
    temp_surgical.disinfect = form['disinfect']
    temp_surgical.bottom = form['bottom']
    temp_surgical.full_etching = form['full_etching']
    temp_surgical.self_etching = form['self_etching']
    temp_surgical.coating_time = form['coating_time']
    temp_surgical.illumination_time = form['illumination_time']
    temp_surgical.resin = form['resin']
    temp_surgical.modification = form['modification']
    temp_surgical.lamp = form['lamp']
    temp_surgical.time_of_lamp = form['time_of_lamp']
    temp_surgical.polishing = form['polishing']
    temp_surgical.appease_medicine = form['appease_medicine']
    temp_surgical.observed_time = form['observed_time']
    temp_surgical.modulo = form['modulo']
    temp_surgical.inlay = form['inlay']
    return temp_surgical


def _form_to_non_surgical(form):
    temp_non_surgical = Non_surgical()
    temp_non_surgical.user_id = form['user_id']
    temp_non_surgical.tooth_id = form['tooth_id']
    temp_non_surgical.handle_type = form['handle_type']
    temp_non_surgical.specific_method = form['specific_method']
    temp_non_surgical.fluorination = form['fluorination']
    temp_non_surgical.silver_nitrate = form['silver_nitrate']
    temp_non_surgical.additional_device = form['additional_device']
    temp_non_surgical.reagent = form['reagent']
    temp_non_surgical.tools = form['tools']
    temp_non_surgical.lamp = form['lamp']
    temp_non_surgical.check_time = form['check_time']
    return temp_non_surgical