import httplib
import json

import flask
from flask import request
from src import app
from src.entity.personal_history import Personal_history
from src.entity.user import User
from src import db

@app.route('/medical-case-of-illness/personal-history',methods=['POST'])
def add_personal_history():
    if _get_user_by_id(request.form['user_id']):
        personal_history = _form_to_personal_history(request.form)
        db.session.add(personal_history)
        db.session.commit()
        response_history = Personal_history.query.filter_by(user_id=request.form['user_id']).first()
        response = response_history.get_dict()
        ret = flask.Response(json.dumps(response))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret

def _get_user_by_id(user_id):
    user = User.query.filter_by(user_id=user_id).all()
    if len(user)<1:
        return False
    else :
        return True

def _form_to_personal_history(form):
    history = Personal_history()
    history.user_id = form['user_id']
    history.consumption_of_sweet = form['consumption_of_sweet']
    history.more_sweet = form['more_sweet']
    history.frequency_of_sweet = form['frequency_of_sweet']
    history.frequency_of_meal = form['frequency_of_meal']
    history.is_carbonic_acid = form['is_carbonic_acid']
    history.is_floss = form['is_floss']
    history.times_of_teeth_brush = form['times_of_teeth_brush']
    history.time_of_teeth_brush = form['time_of_teeth_brush']
    history.long_of_teeth_brush = form['long_of_teeth_brush']
    history.electric_tooth_brush = form['electric_tooth_brush']
    history.method_of_tooth_brush = form['method_of_tooth_brush']
    history.is_fluorine = form['is_fluorine']
    history.is_cavity_examination = form['is_cavity_examination']
    history.is_periodontal_treatment = form['is_periodontal_treatment']
    history.salivary_gland_disease = form['salivary_gland_disease']
    history.sjogren_syndrome = form['sjogren_syndrome']
    history.consciously_reduce_salivary_flow = form['consciously_reduce_salivary_flow']
    history.is_consciously_reduce_salivary_flow = form['is_consciously_reduce_salivary_flow']
    history.is_salivary_gland_disease = form['is_salivary_gland_disease']
    return history

