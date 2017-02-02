# -*- coding:utf-8 -*-
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
            usphs = Usphs.query.filter_by(case_id=request.form['case_id']).all()[-1]
            refresh_step(usphs.case_id, 8)
            res_usphs = Usphs.query.filter_by(case_id=request.form['case_id']).first()
            response = res_usphs.get_dict()
            ret = flask.Response(json.dumps(response))
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret
        else:
            ret = flask.Response("Can't find this user")
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, httplib.BAD_REQUEST
    elif request.method == 'GET':
        temp_result = Usphs.query.filter_by(case_id=request.args['case_id']).first()
        if temp_result:
            response = flask.Response(json.dumps(temp_result.get_dict()))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 200
        else:
            response = flask.Response("Can not find the USPHS...")
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 400
    elif request.method == 'PUT':
        usphs = Usphs.query.filter_by(case_id = request.form['case_id']).first()
        if usphs:
            db.session.query(Usphs).filter(Usphs.case_id == request.form['case_id']).delete()
            db.session.commit()
            temp_usphs = _form_to_usphs(request.form)
            db.session.add(temp_usphs)
            db.session.commit()
            res_usphs = Usphs.query.filter_by(case_id = request.form['case_id']).first()
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
    usphs.tooth_id = form['tooth_id']
    usphs.user_id = form['user_id']
    usphs.case_id = form['case_id']
    usphs.color = form['color']
    usphs.marginal_accuracy = form['marginal_accuracy']
    usphs.anatomic_form = form['anatomic_form']
    usphs.edge_color = form['edge_color']
    usphs.secondary_caries = form['secondary_caries']
    usphs.level = _get_level(form)
    return usphs

def _get_level(form):
    set_A = set(
        [u'无明显颜色变化，色度、饱和度、透明度与邻牙匹配好', u'探针和肉眼均不能检测出间隙，充填体与牙釉质良好接触，边缘无悬突、无着色',
         u'修复体轮廓与牙体组织解剖形态和边缘连续', u'修复体与牙体之间边缘无着色', u'无任何继发龋'])

    set_B = set(
        [u'色度、饱和度、透明度变化，临床可接受', u'探针探有间隙，肉眼可见超出或不足的边缘，边缘有轻微着色，但无牙体或基底材料暴露',
         u'修复体充填稍多或稍欠，未暴露牙本质或基底', u'修复体与牙体之间有变色，但未沿洞缘向牙髓方向渗透', u'可检测到修复体边缘周围继发龋'])

    set_C = set(
        [u'严重色度、饱和度、透明度变化， 临床不可接受', u'探针探有间隙，有牙体或基底材料暴露，但无缺损或脱落',
         u'修复体缺损或缺失，牙本质或基地暴露', u'修复体与牙体之间有变色，沿洞缘向牙髓方向渗透'])

    set_D = set([u'修复体折裂或部分脱落或全部脱落'])

    count_a = 0
    count_b = 0
    count_c = 0
    count_d = 0
    els = 0

    temp_dict = form
    for key , value in temp_dict.items():
        if value in set_A:
            count_a = count_a + 1
        elif value in set_B:
            count_b = count_b + 1
        elif value in set_C:
            count_c = count_c + 1
        elif value in set_D:
            count_d = count_d + 1

    level = ''
    if not count_d == 0:
        level = 'D'
    elif count_d == 0 and count_c != 0:
        level = 'C'
    elif count_d == 0 and count_c == 0 and count_b != 0:
        level = 'B'
    else:
        level = 'A'
    return level