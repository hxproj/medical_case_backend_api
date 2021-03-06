import httplib
import os
import json
import flask
import time
from src.controller.common_function import check_directory, check_file

from src import app
from src import db
from src.entity.illness_case import Illness_case
from src.entity.picture import Picture
from flask import request
from werkzeug import secure_filename
from src.entity.tooth_location import Tooth_location


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

ISOTIMEFORMAT='%Y%m%d%H%M%S'
@app.route('/medical-case-of-illness/img', methods=['GET', 'POST','DELETE','OPTIONS'])
def upload_img():
    if request.method == 'POST':
        response = flask.Response('')
        case_id = request.form["case_id"]
        picture_type = request.form['picture_type']
        case_list = Illness_case.query.filter_by(case_id=case_id).all()
        if case_list:
            files = request.files.getlist("file[]")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename=time.strftime( ISOTIMEFORMAT, time.localtime() )+'_'+filename
                    filepath = check_directory(case_id)

                    flage, path = check_file(case_id, filename)
                    if flage == False:
                        file.save(os.path.join(filepath, filename))
                        pic = Picture()
                        pic.case_id = case_id
                        pic.picture_type = picture_type
                        pic.path = path
                        db.session.add(pic)
                        db.session.commit()
                        response = flask.Response('upload succeed.')
                        response.status_code = 200


                    else:
                        response = flask.Response('upload NOT succeed,The file have been uploaded')
                        response.status_code = 404
        else:
            response = flask.Response('case id not exist')
            response.status_code = 404
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    #return '''
    #<!DOCTYPE html>
    #<title>upload new file</title>
    #<h1>upload file</h1>
    #<form action="" method="POST" enctype="multipart/form-data">
    #<input type="text" name="tooth_id" />tooth_id<br/>
    #<input type="file" name="file[]" multiple="multiple" />
    #<input type="submit" value="upload" />
    #</form>
    #'''
    elif request.method == 'GET':
        case_id=request.args.get('case_id')
        type = request.args['type']
        img_list=Picture.query.filter_by(case_id=case_id,picture_type=type).all()
        path_list=[]
        for img in img_list:
            img=img.get_dict()
            path=img['path']
            path_list.append(img)
        ret = flask.Response(json.dumps(path_list))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'DELETE':
        picture_id = request.args['picture_id']
        picture = Picture.query.filter_by(img_id=picture_id).first()
        try :
            os.remove(picture.path)
        except:
            ret = flask.Response('delete error')
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret,400
        db.session.query(Picture).filter(Picture.img_id ==picture_id).delete()
        db.session.commit()
        ret = flask.Response('delete succeed')
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret, 200
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret