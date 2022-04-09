broker_url='amqp://guest:guest@rabbitmq:5672'
cache_backend='redis://redis:6379/0'
result_backend='redis://redis:6379/1'
imports=['api.exsiccate.tasks']