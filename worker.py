from api import create_app

app = create_app()
app.app_context().push()

from api import celery