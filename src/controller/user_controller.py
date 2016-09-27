import httplib
import json

import datetime
import flask
from flask import request
from src import app
from src.entity.diagnose import Diagnose
from src.entity.difficulty_assessment import Difficulty_assessment
from src.entity.illness_history import Illness_history
from src.entity.non_surgical import Non_surgical
from src.entity.oral_examination import Oral_examination
from src.entity.personal_history import Personal_history
from src.entity.picture import Picture
from src.entity.prognosis_of_management import Prognosis_of_management
from src.entity.risk_assessment import Risk_assessment
from src.entity.surgical import Surgical
from src.entity.tooth_location import Tooth_location
from src.entity.user import User
from src import db
from src.entity.usphs import Usphs


@app.route('/medical-case-of-illness/user/<user_name>',methods=['GET'])
def get_user_by_id(user_name):
    user = User.query.filter_by(name=user_name).all()
    lit =[]
    for temp_user in user:
        lit.append(temp_user.get_dict())
    ret = flask.Response(json.dumps(lit))
    ret.headers['Access-Control-Allow-Origin'] = '*'
    return ret
@app.route('/medical-case-of-illness/user',methods = ['POST','PUT','DELETE'])
def add_user():
    if request.method =='POST':
        if request.form['name'] is not None and request.form['name']!= '' and request.form['contact']!=None:
            current_user = _form_to_user(request.form)
            db.session.add(current_user)
            db.session.commit()
            response_user = User.query.filter_by(name=request.form['name']).first()
            result = response_user.get_dict()
            #result['in_date']=result['in_date'].strftime('%Y-%m-%d %H:%M:%S')
            ret = flask.Response(json.dumps(result))
            ret.headers['Access-Control-Allow-Origin']='*'
            return ret,httplib.OK
        else:
            ret = flask.Response('post error')
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method=='DELETE':
        user_id=request.args['user_id']
        _delete_all(user_id)
        ret = flask.Response('OK')
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret, httplib.OK
    elif request.method =='PUT':
        if request.form['name'] is not None and request.form['name'] != '' and request.form['contact'] != None:
            db.session.query(User).filter(User.user_id==request.form['user_id']).delete()
            user = _form_to_user_update(request.form)
            db.session.commit()
            db.session.add(user)
            db.session.commit()
            res_user = User.query.filter_by(user_id = request.form['user_id']).first()
            response = res_user.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.OK
        else:
            ret = flask.Response('post error')
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST

def _form_to_user(form):
    user = User()
    user.age = form['age']
    user.contact = form['contact']
    user.gender = form['gender']
    user.name = form['name']
    user.occupation = form['occupation']
    user.in_date = datetime.datetime.now()
    return user

def _form_to_user_update(form):
    user = _form_to_user(form)
    user.user_id = form['user_id']
    return user

def _delete_all(user_id):
    db.session.query(User).filter(User.user_id==user_id).delete()
    tooth_list=db.session.query(Tooth_location.tooth_id).filter(Tooth_location.user_id==user_id).all()
    if tooth_list:
        for temp in tooth_list:
            db.session.query(Picture).filter(Picture.tooth_id==temp).delete()
    db.session.query(Usphs).filter(Usphs.user_id == user_id).delete()
    db.session.query(Tooth_location).filter(Tooth_location.user_id == user_id).delete()
    db.session.query(Surgical).filter(Surgical.user_id == user_id).delete()
    db.session.query(Risk_assessment).filter(Risk_assessment.user_id == user_id).delete()
    db.session.query(Prognosis_of_management).filter(Prognosis_of_management.user_id == user_id).delete()
    db.session.query(Personal_history).filter(Personal_history.user_id == user_id).delete()
    db.session.query(Oral_examination).filter(Oral_examination.user_id == user_id).delete()
    db.session.query(Non_surgical).filter(Non_surgical.user_id == user_id).delete()
    db.session.query(Illness_history).filter(Illness_history.user_id == user_id).delete()
    db.session.query(Difficulty_assessment).filter(Difficulty_assessment.user_id == user_id).delete()
    db.session.query(Diagnose).filter(Diagnose.user_id == user_id).delete()
    db.session.commit()