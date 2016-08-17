import httplib
import json

import flask
from flask import request
from src import app
from src.entity.user import User
from src import db


@app.route('/medical-case-of-illness/user/<user_id>',methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    dit = user.get_dict()
    ret = flask.Response(json.dumps(dit))
    ret.headers['Access-Control-Allow-Origin'] = '*'
    return ret
@app.route('/medical-case-of-illness/user/',methods = ['POST'])
def add_user():
    if request.form['name']!=None:
        current_user = _form_to_user(request.form)
        db.session.add(current_user)
        db.session.commit()
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin']='*'
        return ret,httplib.OK
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
    return user
