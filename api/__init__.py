from celery import Celery
import celery_config as cel



def make_celery():
    return Celery(__name__,broker_url=cel.broker_url, cache_backend=cel.cache_backend, result_backend=cel.result_backend, imports = cel.imports)

celery = make_celery()