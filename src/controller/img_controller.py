import httplib
import os
import json
import flask
import time
from src.controller.common_function import check_directory, check_file

from src import app
from src import db
from src.entity.picture import Picture
from flask import request
from werkzeug import secure_filename
from src.entity.tooth_location import Tooth_location


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

ISOTIMEFORMAT='%Y%m%d%H%M%S'
@app.route('/medical-case-of-illness/img', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        response = flask.Response('')
        tooth_id = request.form["tooth_id"]
        tooth_list = Tooth_location.query.filter_by(tooth_id=tooth_id).all()
        if tooth_list:
            files = request.files.getlist("file[]")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename=time.strftime( ISOTIMEFORMAT, time.localtime() )+'_'+filename
                    filepath = check_directory(tooth_id)

                    flage, path = check_file(tooth_id, filename)
                    if flage == False:
                        file.save(os.path.join(filepath, filename))
                        pic = Picture()
                        pic.tooth_id = tooth_id
                        pic.path = path
                        db.session.add(pic)
                        db.session.commit()
                        response = flask.Response('upload succeed.')
                        response.status_code = 200


                    else:
                        response = flask.Response('upload NOT succeed,The file have been uploaded')
                        response.status_code = 404
        else:
            response = flask.Response('toothid not exist')
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
    if request.method == 'GET':
        tooth_id=request.args.get('tooth_id')
        img_list=Picture.query.filter_by(tooth_id=tooth_id).all()
        path_list=[]
        for img in img_list:
            img=img.get_dict()
            path=img['path']
            path_list.append(path)
        ret = flask.Response(json.dumps(path_list))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
