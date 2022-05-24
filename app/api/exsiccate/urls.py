#python imports
from os import path, mkdir, walk, listdir
from uuid import uuid4, UUID
import time
#frameworks imports
from functools import wraps
from marshmallow import ValidationError, EXCLUDE
from flask import current_app as app
from flask import jsonify, request, make_response, abort
from flask.views import  MethodView
from flask.wrappers import Response
from webargs.flaskparser import parser
from marshmallow import fields
from api.images import getImages, requestImageDir
#app imports
from api.serializers\
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
        print('json::::::',request.form)
        try:
            data = request.form.copy()
            data = ExsiccateSerializer().loads(data['json'])
            # print(request.form)
            files = request.files.copy()
            print(files.keys())
            if files is not None:
                tax,loc,col= data['taxonomy'],data['location'],data['collector']
                tax,loc,col= TaxonomySerializer().load(tax),LocationSerializer().load(loc),CollectorSerializer().load(col)
                resp = exsiccate.insert.apply_async(args = (tax,loc,col))
                id_exsiccate = resp.wait()
                for i in files:
                    extension = files[i].filename.split('.')[-1]
                    savePath = exsiccate.saveImages.s(id_exsiccate,extension ).apply_async().wait()
                    print(savePath)
                    files[i].save(savePath)
                return jsonify({'status': id_exsiccate})
        except ValidationError as err:
            print('Validation Error')
            return jsonify({'status' : err.errors})
    def get(self, *args, **kwargs):
        _args = parser.parse(ExsiccateSerializer(),request,unknown=EXCLUDE,location='querystring')
        image_list = []
        result = None
        if _args is not None:
            exs = exsiccate.search.apply_async(args=[_args])
            # dir = path.join(app.config['UPLOAD_FOLDER']+ UUID(exs[0]['id_exsiccate']).hex)
            # i = None
            # if path.isdir(dir):
            #     for root, dirs, files in walk(dir, topdown=False):
            #         # result  = send_file((root+'/'+ i for i in files), mimetype='image/png',as_attachment=True)
            #         for i in files:
            #             result = send_file(root+'/'+i, mimetype='image/png',as_attachment=True)
            #             print(result)
            # response = {
            #     'json': jsonify(exs),
            #     'images': result
            # }
            if len(exs.get()) == 0:
                getImages(app.config['UPLOAD_FOLDER'])
                requestImageDir('944475cb-36a0-4096-acc9-819441e6221a')
                return jsonify('sem dados')
            return jsonify(exs.get())
        else:
            exs = exsiccate.search.apply_async()
            # response = make_response(Response(response = {'data': json.dumps(exs.get())},headers ={'Accept-Encoding': '*'},mimetype = 'multipart/form-data'))
            # print(response)
            requestImageDir('944475cb-36a0-4096-acc9-819441e6221a')
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
