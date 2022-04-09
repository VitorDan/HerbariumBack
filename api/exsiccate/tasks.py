from api import celery, socket
from webargs.flaskparser import parser
from .serializers import ExsiccateSerializer, TaxonomySerializer, CollectorSerializer,LocationSerializer
from .models import Taxonomy, Collector, Location, Exsiccate
from flask import current_app as app


@celery.task()#decorator
def search(params = None, *args, **kwargs):
    with app.app_context():
        if params :
            if 'id_exsiccate' not in params.keys():
                dumps = Exsiccate.query.join(Exsiccate.taxon).filter_by(**params['taxonomy'] if 'taxonomy' in params.keys() else {})\
                                .join(Exsiccate.loco).filter_by(**params['location'] if 'location' in params.keys() else {})\
                                .join(Exsiccate.col).filter_by(**params['collector'] if 'collector' in params.keys() else {})
                dumps = ExsiccateSerializer(many=True).dump(dumps)
                return dumps
            else:
                dumps = Exsiccate.query.filter_by(id_exsiccate=params['id_exsiccate']).join(Exsiccate.taxon).filter_by(**params['taxonomy'] if 'taxonomy' in params.keys() else {})\
                                .join(Exsiccate.loco).filter_by(**params['location'] if 'location' in params.keys() else {})\
                                .join(Exsiccate.col).filter_by(**params['collector'] if 'collector' in params.keys() else {})
            
                dumps = ExsiccateSerializer(many=True).dump(dumps)
                return dumps
        else:
            dumps = Exsiccate().query.all()
            dumps = ExsiccateSerializer(many=True).dump(dumps)
            return dumps

@celery.task()#decorator
def insert(tax=None,loc=None, col = None):
    print(tax)
    with app.app_context():
        taxonomy = Taxonomy(**tax)
        if taxonomy:
            taxonomy.save()
        location = Location(**loc)
        if location:
            location.save()
        collector = Collector(**col)
        if collector:
            collector.save()
        exsiccate = Exsiccate(**{'id_taxonomy':taxonomy.id_taxonomy,'id_location':location.id_location,'id_collector':collector.id_collector})
        if exsiccate:
            exsiccate.save()
            return exsiccate.id_exsiccate
@celery.task() #decorator
def delete(id):
    with app.app_context():
        exsiccate = Exsiccate.query.filter_by(**id).first()
        if exsiccate:
            exsiccate.destroy()
            return 'Sucesso.'
        return 'Error ao apagar.'
@celery.task() #decorator
def update(id, params):
    with app.app_context():
        exsiccate = Exsiccate.query.filter_by(**id).first()
        if 'taxonomy' in params.keys():
            tax = Taxonomy.query.filter_by(id_taxonomy =exsiccate.taxon.id_taxonomy).update(params['taxonomy'])
            if tax:
                exsiccate.taxon.committed()
        if 'location'in params.keys():
            loc = Location.query.filter_by(id_location = exsiccate.loco.id_location).update(params['location'])
            if loc:
                exsiccate.loco.committed()
        if 'collector' in params.keys():
            col = Collector.query.filter_by(id_collector = exsiccate.col.id_collector).update(params['collector'])
            if col:
                exsiccate.col.committed()
        exsiccate.committed()
