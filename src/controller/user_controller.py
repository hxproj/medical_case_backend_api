import httplib
import json

import datetime
import flask
from flask import request
from src import app
from src.entity.user import User
from src import db


@app.route('/medical-case-of-illness/user/<user_name>',methods=['GET'])
def get_user_by_id(user_name):
    user = User.query.filter_by(name=user_name).all()
    lit =[]
    for temp_user in user:
        lit.append(temp_user.get_dict())
    ret = flask.Response(json.dumps(lit))
    ret.headers['Access-Control-Allow-Origin'] = '*'
    return ret
@app.route('/medical-case-of-illness/user',methods = ['POST','PUT'])
def add_user():
    if request.method =='POST':
        if request.form['name'] is not None and request.form['name']!= '' and request.form['contact']!=None:
            current_user = _form_to_user(request.form)
            db.session.add(current_user)
            db.session.commit()
            response_user = User.query.filter_by(name=request.form['name']).first()
            result = response_user.get_dict()
            ret = flask.Response(json.dumps(result))
            ret.headers['Access-Control-Allow-Origin']='*'
            return ret,httplib.OK
        else:
            ret = flask.Response('post error')
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
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