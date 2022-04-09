broker_url='amqp://guest:guest@172.17.0.1:5672//'
cache_backend='redis://172.17.0.1:6379/0'
result_backend='redis://172.17.0.1:6379/1'
imports=['api.exsiccate.tasks']