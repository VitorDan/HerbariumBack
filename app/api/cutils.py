import celery_config as c 
def init_celery(app,celery):
    celery.conf.update(app.config)
    BaseTask = celery.Task
    class ContextTask(BaseTask):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return BaseTask.__call__(self, *args, **kwargs)
    celery.Task = ContextTask