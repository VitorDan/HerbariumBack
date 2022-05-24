accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
broker_url='amqp://guest:guest@localhost:5672'
cache_backend='redis://localhost:6379/0'
result_backend='redis://localhost:6379/1'
imports=['api.exsiccate.tasks','api.images.path']