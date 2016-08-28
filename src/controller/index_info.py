import httplib
import json
import flask
from flask import request
from src import app
from src.entity.tooth_location import Tooth_location
from src.entity.user import User
from src.controller.common_function import check_if_user_exist, refresh_step
from src import db

@app.route('/medical-case-of-illness/index-info',methods=['GET'])
def get_index():
    page = request.args['page']
    user_list = db.session.query(User)
    