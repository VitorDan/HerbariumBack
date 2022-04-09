from api import celery
from api.factory import create_app
from api.cutils import init_celery
app = create_app()
init_celery(app, celery)