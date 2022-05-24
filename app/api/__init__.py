from celery import Celery
import celery_config as cel



def make_celery():
    _celery =  Celery(__name__,broker_url=cel.broker_url, cache_backend=cel.cache_backend, result_backend=cel.result_backend, imports = cel.imports)
    _celery.conf.update(
        task_serializer="pickle",
        result_serializer="pickle",
        accept_content=["pickle","json"]
    )
    return _celery
celery = make_celery()