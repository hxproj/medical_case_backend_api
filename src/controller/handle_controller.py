import httplib
import json
import flask
from flask import request
from src import app
from src.entity.surgical import Surgical
from src.entity.non_surgical import Non_surgical
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db


@app.route('/medical-case-of-illness/handle', methods=['POST', 'PUT', 'GET','OPTIONS'])
def handle_method():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            handle_type = int(request.form['handle_type'])
            if handle_type == 0:
                non_surgical = _form_to_non_surgical(request.form)
                db.session.add(non_surgical)
                db.session.commit()
                handle = Non_surgical.query.filter_by(user_id=request.form['user_id']).all()[-1]
                refresh_step(handle.case_id, 6)
                ret_non_surgical = Non_surgical.query.filter_by(case_id=request.form['case_id']).first()
                response = ret_non_surgical.get_dict()
                ret = flask.Response(json.dumps(response))
                ret.headers['Access-Control-Allow-Origin'] = '*'
                return ret
            elif handle_type == 1 or handle_type == 2 or handle_type == 3 or handle_type == 4:
                surgical = _form_to_surgical(request.form)
                db.session.add(surgical)
                db.session.commit()
                handle = Surgical.query.filter_by(user_id=request.form['user_id']).all()[-1]
                refresh_step(handle.case_id, 6)
                ret_surgical = Surgical.query.filter_by(case_id=request.form['case_id']).first()
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
        query_result = Surgical.query.filter_by(case_id=request.args['case_id']).first()
        if query_result:
            ret = flask.Response(json.dumps(query_result.get_dict()))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            query_result = Non_surgical.query.filter_by(case_id=request.args['case_id']).first()
            if query_result:
                ret = flask.Response(json.dumps(query_result.get_dict()))
                ret.headers['Access-Control-Allow-Origin'] = '*'
                return ret, 200
            else:
                response = flask.Response("Can not find the cure...")
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response, 400
    elif request.method == 'PUT':
        if check_if_user_exist(request.form['user_id']):
            if int(request.form['handle_type']) == 0:
                temp_result = _form_to_non_surgical(request.form)
            else:
                temp_result = _form_to_surgical(request.form)
            db.session.query(Surgical).filter(
                Surgical.case_id == request.form['case_id']).delete()
            db.session.query(Non_surgical).filter(
                Non_surgical.case_id == request.form['case_id']).delete()
            db.session.commit()
            db.session.add(temp_result)
            db.session.commit()
            if int(request.form['handle_type']) == 0:
                result = Non_surgical.query.filter_by(case_id=request.form['case_id']).first()
            else:
                result = Surgical.query.filter_by(case_id=request.form['case_id']).first()
            response = result.get_dict()
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


def _form_to_surgical(form):
    temp_surgical = Surgical()
    temp_surgical.user_id = form['user_id']
    temp_surgical.tooth_id = form['tooth_id']
    temp_surgical.case_id = form['case_id']
    temp_surgical.handle_type = form['handle_type']
    temp_surgical.specific_method = form['specific_method']

    temp_surgical.anesthesia_medicine = form.get('anesthesia_medicine')
    temp_surgical.part_anesthesia = form.get('part_anesthesia')
    temp_surgical.rubber = form.get('rubber')
    temp_surgical.microscope = form.get('microscope')
    temp_surgical.tools = form.get('tools')
    temp_surgical.shape_of_hole = form.get('shape_of_hole')
    temp_surgical.depth_of_hole = form.get('depth_of_hole')
    temp_surgical.is_piece = form.get('is_piece')
    temp_surgical.is_chock = form.get('is_chock')
    temp_surgical.shade_guide = form.get('shade_guide')
    temp_surgical.color_of_tooth = form.get('color_of_tooth')
    temp_surgical.disinfect = form.get('disinfect')
    temp_surgical.bottom = form.get('bottom')
    temp_surgical.etching_type = form.get('etching_type')
    temp_surgical.full_etching = form.get('full_etching')
    temp_surgical.self_etching = form.get('self_etching')
    temp_surgical.coating_time = form.get('coating_time')
    temp_surgical.illumination_time = form.get('illumination_time')
    temp_surgical.resin = form.get('resin')
    temp_surgical.color_of_resin = form.get('color_of_resin')
    temp_surgical.modification = form.get('modification')
    temp_surgical.lamp = form.get('lamp')
    temp_surgical.time_of_lamp = form.get('time_of_lamp')
    temp_surgical.appease_medicine = form.get('appease_medicine')
    temp_surgical.observed_time = form.get('observed_time')
    temp_surgical.modulo = form.get('modulo')
    temp_surgical.inlay = form.get('inlay')
    temp_surgical.compromise = form.get('compromise')
    temp_surgical.polishing = form.get('polishing')
    temp_surgical.drill_needle = form.get('drill_needle')
    temp_surgical.gingival_retraction = form.get('gingival_retraction')
    temp_surgical.additional = form.get('additional')
    temp_surgical.compromise_polishing_additional = form.get('compromise_polishing_additional')

    #additional parameters
    temp_surgical.dry_times = form.get('dry_times')
    temp_surgical.acid_time = form.get('acid_time')
    temp_surgical.fluoride_protector = form.get('fluoride_protector')
    temp_surgical.is_micro = form.get('is_micro')
    temp_surgical.low_mobile = form.get('low_mobile')
    temp_surgical.micro = form.get('micro')
    temp_surgical.penetration_resin = form.get('penetration_resin')

    temp_surgical.prosthesis_type = form.get('prosthesis_type')
    temp_surgical.fill_material = form.get('fill_material')
    temp_surgical.bind_material = form.get('bind_material')
    temp_surgical.bind_type = form.get('bind_type')
    temp_surgical.bind_type_component = form.get('bind_type_component')
    temp_surgical.fluoride_acid_time = form.get('fluoride_acid_time')
    temp_surgical.phosphorus_acid_time = form.get('phosphorus_acid_time')
    temp_surgical.silicon = form.get('silicon')

    temp_surgical.glass_ionomer = form.get('glass_ionomer')

    return temp_surgical


def _form_to_non_surgical(form):
    temp_non_surgical = Non_surgical()
    temp_non_surgical.user_id = form['user_id']
    temp_non_surgical.tooth_id = form['tooth_id']
    temp_non_surgical.case_id = form['case_id']
    temp_non_surgical.handle_type = form['handle_type']
    temp_non_surgical.specific_method = form['specific_method']

    temp_non_surgical.fluorination = form.get("fluorination")
    temp_non_surgical.silver_nitrate = form.get("silver_nitrate")
    temp_non_surgical.additional_device = form.get("additional_device")
    temp_non_surgical.reagent = form.get("reagent")
    temp_non_surgical.non_surgical_tools = form.get("non_surgical_tools")
    temp_non_surgical.non_surgical_lamp = form.get("non_surgical_lamp")
    temp_non_surgical.check_time = form.get("check_time")
    temp_non_surgical.time_of_etching = form.get("time_of_etching")
    temp_non_surgical.non_surgical_coating_time = form.get("non_surgical_coating_time")

    return temp_non_surgical