from functools import wraps
import jwt
from flask import request, abort
from flask import current_app as app
from api.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Token inexistente!",
                "data": None,
                "error": "Não Autoriazado"
            }, 401
        try:
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user= User.query.find_by(id_user = data["user_id"]).first()
            if current_user is None:
                return {
                "message": "Token invalido!",
                "data": None,
                "error": "Não autorizado"
            }, 401
            if not current_user["active"]:
                abort(403)
        except Exception as e:
            return {
                "message": "Deu algo errado!!",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)
    return decorated