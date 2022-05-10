from api import factory
import api
app = factory.create_app(celery=api.celery)
if __name__ == '__main__':
    from api.factory import core
    app.run()