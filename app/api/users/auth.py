from functools import wraps
from flask.views import MethodView
from flask import request
def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get("Authorization") == "Bearer 12345":
            return fn(*args, **kwargs)
        else:
            abort(401)

    return wrapper



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