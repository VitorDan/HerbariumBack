#python imports
from os import path, mkdir, walk, listdir
from uuid import uuid4, UUID
import time
#frameworks imports
from functools import wraps
from marshmallow import ValidationError
from flask import current_app as app
from flask import jsonify, request, make_response, abort
from flask.views import  MethodView
from  flask.wrappers import Response
from webargs.flaskparser import parser
from marshmallow import fields
#app imports
from api.exsiccate.models import Exsiccate
from .serializers\
     import CollectorSerializer, LocationSerializer, TaxonomySerializer, ExsiccateSerializer
from api.exsiccate import tasks as exsiccate


response = {'id_collector': 'e77ba4d5-fb11-400d-8563-c2e83a860ba4', 'collector_name': 'Vitor Daniel Leal', 'collector_foundation': 'IFMG', 'collector_cite': 'Leal; V.D.', 'collector_birthday': None, 'collector_mail':'plante_com_amor@gmail.com', 'collector_office': None} 
def auth_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get("Authorization") == "Bearer 12345":
            return fn(*args, **kwargs)
        else:
            abort(401)

    return wrapper

class ExsiccateRoute(MethodView):
    methods =['POST', 'GET', 'DELETE', 'PUT']
    def post(self,*args,**kwargs):
        print(request.__dict__)
        try:
            data = parser.parse(ExsiccateSerializer(), request,location='json_or_form')
            print('ate aqui foi')
            if request.files:
                print('Request: ',request.__dict__)
                tax,loc,col= data['taxonomy'],data['location'],data['collector']
                tax,loc,col= TaxonomySerializer().load(tax),LocationSerializer().load(loc),CollectorSerializer().load(col)
                resp = exsiccate.insert.apply_async(args = (tax,loc,col))
                #inside task
                resp = resp.get()
                dir = path.join(app.config['UPLOAD_FOLDER'])
                files = request.files
                if resp not in listdir(dir):
                    mkdir(dir+'/'+resp)
                    for i in files:
                        files[i].save(path.join(dir+'/'+resp, uuid4().hex + '.png'))
                    # return jsonify({'status' : "Exsicata Salva"})
                    return jsonify({'status' : resp})

                else:
                   return jsonify({'status':'isso n deveria acontecer'})   
        except ValidationError as err:
            return jsonify({'status' : err.errors})
    def get(self, *args, **kwargs):
        print('nunca nem vi')
        _args = parser.parse(ExsiccateSerializer(),request,location='json')
        image_list = []
        result = None
        if _args:
            exs = exsiccate.search.apply_async(params =_args)
            dir = path.join(app.config['UPLOAD_FOLDER']+ UUID(exs[0]['id_exsiccate']).hex)
            i = None
            if path.isdir(dir):
                for root, dirs, files in walk(dir, topdown=False):
                    # result  = send_file((root+'/'+ i for i in files), mimetype='image/png',as_attachment=True)
                    for i in files:
                        result = send_file(root+'/'+i, mimetype='image/png',as_attachment=True)
                        print(result)      
            response = {
                'json': jsonify(exs),
                'images': result
            }
            if len(exs.get()) == 0:
                return jsonify('sem dados')
            return jsonify(exs.get())
        else:
            exs = exsiccate.search.apply_async()
            # response = make_response(Response(response = {'data': json.dumps(exs.get())},headers ={'Accept-Encoding': '*'},mimetype = 'multipart/form-data'))
            # print(response)
            print(len(exs.get()))
            if len(exs.get()) == 0:
                return jsonify('sem dados')
            return jsonify(exs.get())
    def delete(self, *args,**kwargs):
        id = parser.parse({'id_exsiccate': fields.UUID()}, request, location='querystring')
        print(type(id))
        returned = exsiccate.delete.apply_async(args=[id])
        return jsonify({'status':returned.get()})
    def put(self, *args,**kwargs):
        id = parser.parse({'id_exsiccate': fields.UUID()}, request, location='querystring')
        _args = parser.parse(ExsiccateSerializer(),request,location='json')
        exsiccate.update.apply_async(id = id, params = _args)
        time.sleep(0.5)
        return jsonify({'status': 'Due'})

class LoginRoute(MethodView):
    methods = ['POST','GET']
    def post(self,**kwargs):
        if (request.json["email"] == "plante_com_amor@gmail.com" and request.json["password"] == "12345"):
            return jsonify({'token': '2wsadsadklakdl'})
        abort(400)
    @auth_required
    def get(self, **kwargs):
        print(request.headers)
        return jsonify(response)
# @socket.on('connect')
# def connectExsiccate(*args, **kwargs):
#     print('connected')

# @socket.on('connect', namespace='/exsiccate')
# def connectExsiccate():
#     print('connected')
# @socket.on('search', namespace='/exsiccate')
# def search_socks():
#     print('ola mundo')
#     search.apply_async()