from crypt import methods
import jwt
from flask import current_app as app
from flask import jsonify, request
from api.auth import token_required
from api.models import User
from api.users.tasks import setUser, loginUser

@app.route('/auth/', methods=['GET'])
def auth():
    return f'<p>Ola Mundo</p>'
@app.route('/auth/user/')
@token_required
def currentUser(current_user):
    return jsonify(current_user)
@app.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.form
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        user = loginUser.apply_async(args=[data]).wait()
        if user == -1:
            return jsonify('error')
        return jsonify(user)
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500

@app.route("/auth/singup", methods = ["POST"])
def singup():
    data = request.form.copy()
    id = setUser.apply_async(args=[data])
    return jsonify(id.wait())

