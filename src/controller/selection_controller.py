import json
from operator import and_

from src import app
from src import db
from flask import request
import flask
from src.entity.selections import Selection

@app.route('/medical-case-of-illness/selections', methods=['POST', 'PUT', 'GET','DELETE','OPTIONS'])
def handle_selections():
    if request.method == 'POST':
        selection = Selection()
        selection.field = request.form['filed']
        selection.table_name = request.form['table_name']
        selection.value = request.form['value']
        db.session.add(selection)
        db.session.commit()
        response_selection  = Selection.query.all()[-1]
        response = json.dumps(response_selection.get_dict())
        ret = flask.Response(response)
        ret.headers['Access-Control-Allow-Origin'] = '*'
        return ret,200
    elif request.method == 'GET':
        filed = request.args.get('filed')
        table_name = request.args.get('table_name')
        id = request.args.get('id')
        selection_list =[]
        if id != None :
            id = int(id)
            result = Selection.query.filter_by(id = id).first()
            if result:
                selection_list.append(result.get_dict())
        elif id == None:
            if filed ==None:
                result_list = Selection.query.filter_by(table_name = table_name).all()
                for result in result_list:
                    selection_list.append(result.get_dict())
            elif filed !=None:
                result_list = db.session.query(Selection).filter(and_(Selection.table_name == table_name,Selection.field == filed)).all()
                for result in result_list:
                    selection_list.append(result.get_dict())
        ret = flask.Response(json.dumps(selection_list))
        return ret,200
    elif request.method =='DELETE':
        id = request.args.get('id')
        if db.session.query(Selection).filter(Selection.id==int(id)).delete():
            db.session.commit()
            return 'delete success',200
        else:
            return 'error',403
    elif request.method == 'OPTIONS':
        ret = flask.Response()
        ret.headers['Access-Control-Allow-Origin'] = '*'
        ret.headers['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return ret