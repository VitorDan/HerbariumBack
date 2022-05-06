from werkzeug.security import generate_password_hash, check_password_hash
from flask.views import MethodView
from flask import request, jsonify
from api.factory import login_manager as manager
from flask_login import login_user, logout_user, login_required
from api.users.models import User
from flask import current_app as app

@app.route('/manager/login', methods=['POST'])
def login():
    print('ola')
    mail,password =  request.form.get('email'), request.form.get('password')
    collector = User.query.filter_by(user_mail=mail).first()
    if not collector or not check_password_hash(collector.user_password,password):
        return jsonify('Not User')
    login_user(collector)
    return jsonify(collector.user_id)
@app.route('/manager/singup', methods=['POST'])
def singup():
    name,mail,password =  request.form.get('name'), request.form.get('email'),request.form.get('password')
    collector = User.query.filter_by(user_mail=mail)
    if not collector:
        return jsonify('usuario ja existe')
    collector = User(user_name=name,user_mail=mail,user_password =generate_password_hash(password,method='sha256'))
    if collector is not None:
        collector.save()
        return jsonify('Sucesso')
    return 'porra'



class Login(MethodView):
    methods = ['POST','GET']
    def post(self):
        mail,password =  request.form.get('email'), request.form.get('password')
        collector = User.query.filter_by(user_mail=mail).first()
        if not collector or not check_password_hash(collector.user_password,password):
            return jsonify('Not User')
        login_user(collector)
        return jsonify(collector.user_id)
    def get(self, **kwargs):
        pass