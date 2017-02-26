import os
import json
import flask
import time
import datetime
from src.controller.common_function import check_directory, check_file

from src import app
from src import db
from src.entity.file import File
from flask import request
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/medical-case-of-illness/file', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def upload_file():
    if request.method == 'POST':
        response = flask.Response('')
        files = request.files.getlist("file[]")
        if files:
            for this_file in files:
                origin_file_name = this_file.filename
                secure_file_name = secure_filename(origin_file_name)
                if "." not in secure_file_name:
                    secure_file_name = "." + secure_file_name
                file_save_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '_' + secure_file_name
                file_path = check_directory("help_document")

                flag, path = check_file("help_document", file_save_name)
                if not flag:
                    this_file.save(os.path.join(file_path, file_save_name))

                    temp_file = File()
                    temp_file.name = origin_file_name[:origin_file_name.rfind(".")]
                    temp_file.path = path
                    temp_file.in_date = datetime.datetime.now()

                    db.session.add(temp_file)
                    db.session.commit()
                    response = flask.Response('upload file success...')
                    response.status_code = 200
                else:
                    response = flask.Response('upload failed, The file have been uploaded...')
                    response.status_code = 404
        else:
            response = flask.Response('the file of upload is empty...')
            response.status_code = 404

        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    elif request.method == 'GET':
        file_id = request.args.get('file_id')
        if file_id:
            this_file = File.query.filter_by(file_id=file_id).first()
            ret = flask.Response(json.dumps(this_file.get_dict()))
        else:
            files = File.query.all()
            file_list = []
            for this_file in files:
                file_info = {}
                file_info["file_id"] = this_file.file_id
                file_info["name"] = this_file.name
                file_info["path"] = this_file.path
                file_info["in_date"] = this_file.in_date.strftime('%Y-%m-%d %H:%M')
                file_list.append(file_info)
            ret = flask.Response(json.dumps(file_list))
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'PUT':
        file_id = request.form['file_id']
        file_name = request.form['name']
        File.query.filter_by(file_id=file_id).update(dict(name=file_name))
        db.session.commit()

        ret = flask.Response('edit file succeed...')
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    elif request.method == 'DELETE':
        file_id = request.args['file_id']
        this_file = File.query.filter_by(file_id=file_id).first()
        try:
            os.remove(this_file.path)
        except:
            ret = flask.Response('delete error')
            ret.headers['Access-Control-Allow-Origin'] = '*'
            return ret, 400
        db.session.query(File).filter(File.file_id == file_id).delete()
        db.session.commit()
        ret = flask.Response('delete succeed...')
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret, 200
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret