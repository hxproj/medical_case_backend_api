import httplib
import json
import flask
from flask import request
from src import app
from src.entity.usphs import Usphs
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db


@app.route('/medical-case-of-illness/usphs', methods=['POST', 'PUT', 'GET', 'OPTIONS'])
def usphs_method():
    if request.method == 'POST':
        if check_if_user_exist(request.form['user_id']):
            temp_usphs = _form_to_usphs(request.form)
            db.session.add(temp_usphs)
            db.session.commit()
            usphs = Usphs.query.filter_by(user_id=request.form['user_id']).all()[-1]
            refresh_step(usphs.tooth_id, 6)
            res_usphs = Usphs.query.filter_by(tooth_id=request.form['tooth_id']).first()
            response = res_usphs.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'GET':
        temp_result = Usphs.query.filter_by(tooth_id=request.args['tooth_id']).first()
        response = temp_result.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'PUT':
        usphs = Usphs.query.filter_by(tooth_id = request.form['tooth_id']).first()
        if usphs:
            db.session.query(Usphs).filter(Usphs.tooth_id == request.form['tooth_id']).delete()
            db.session.commit()
            temp_usphs = _form_to_usphs(request.form)
            db.session.add(temp_usphs)
            db.session.commit()
            res_usphs = Usphs.query.filter_by(tooth_id = request.form['tooth_id']).first()
            response = flask.Response(json.dumps(res_usphs.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return  response,200
        else:
            response = flask.Response('can not find this record.')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret


def _form_to_usphs(form):
    usphs = Usphs()
    usphs.color = form['color']
    usphs.tooth_id = form['tooth_id']
    usphs.user_id = form['user_id']
    usphs.marginal_accuracy = form['marginal_accuracy']
    usphs.anatomic_form = form['anatomic_form']
    usphs.surfaceness = form['surfaceness']
    usphs.edge_color = form['edge_color']
    usphs.occlusal_contact = form['occlusal_contact']
    usphs.sensitivity_of_tooth = form['sensitivity_of_tooth']
    usphs.secondary_caries = form['secondary_caries']
    usphs.integrity = form['integrity']
    return usphs
