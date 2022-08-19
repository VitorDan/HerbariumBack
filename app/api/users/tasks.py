import jwt
from flask import current_app as app
from werkzeug.security import generate_password_hash as generate, check_password_hash as check
from api import celery
from api.models import User
from api.serializers import UserSerializer

@celery.task()
def setUser(params):
    with app.app_context():
        user = User.query.filter_by(user_mail = params['user_mail']).first()
        if user is not None:
            return 'usuario ja exite'
        else:
            params['user_pass'] = generate(params['user_pass'])
            user = User(**params)
            if user is not None:
                user.save()
                return user.id_user
        return 'error'
@celery.task()
def loginUser(params):
    with app.app_context():
        user = User.query.filter_by(user_mail = params['user_mail']).first()
        if not user or not check(user.user_pass,params['user_pass']):
            return -1
        token = jwt.encode(
            {'id_user': user.id_user.hex},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        User.query.filter_by(user_mail = params['user_mail']).update({'user_token': token})
        user.committed()
        return token