import json
from api import ma_instance as ma
from .models import Taxonomy, Location, Collector, Exsiccate, db
from sqlalchemy.orm import sessionmaker
from marshmallow import pre_load, post_dump
Session = sessionmaker(bind=db)
class TaxonomySerializer(ma.SQLAlchemySchema):
    id_taxonomy = ma.auto_field()
    kingdom = ma.auto_field()
    phylum = ma.auto_field()
    e_class = ma.auto_field()
    order = ma.auto_field()
    family = ma.auto_field()
    genus = ma.auto_field()
    specific_epithet = ma.auto_field()
    class Meta:
        model = Taxonomy
        sqla_session = Session
        ordered = True 
class LocationSerializer(ma.SQLAlchemySchema):
    id_location = ma.auto_field()
    country = ma.auto_field()
    stateprovince = ma.auto_field()
    city = ma.auto_field()
    county = ma.auto_field()
    latitude = ma.auto_field()
    longitude = ma.auto_field()
    elevation = ma.auto_field()
    class Meta:
        model = Location
        sqla_session = Session
        ordered = True 
class CollectorSerializer(ma.SQLAlchemySchema):
    id_collector = ma.auto_field()
    collector_name = ma.auto_field()
    collector_foundation = ma.auto_field()
    collector_cite = ma.auto_field()
    collector_birthday = ma.auto_field()
    collector_mail = ma.auto_field()
    collector_office = ma.auto_field()

    class Meta:
        model = Collector
        sqla_session = Session
        ordered = True 
class ExsiccateSerializer(ma.SQLAlchemySchema):
    id_exsiccate = ma.auto_field()
    id_taxonomy = ma.auto_field()
    id_location = ma.auto_field()
    id_collector = ma.auto_field()
    taxonomy = ma.Nested(TaxonomySerializer)
    location= ma.Nested(LocationSerializer)
    collector = ma.Nested(CollectorSerializer)
    
    @pre_load
    def pre_processes(self,data, **kwargs):
        if 'exsiccate' in data.keys():
            data_transformed  = json.loads(data['exsiccate'])
            return data_transformed
        else: 
            return data
    @post_dump
    def post_process(self,data,**kwargs):
        tax = Taxonomy.query.filter_by(id_taxonomy = data['id_taxonomy']).first()
        loc = Location.query.filter_by(id_location = data['id_location']).first()
        col = Collector.query.filter_by(id_collector = data['id_collector']).first()
        tax = TaxonomySerializer().dump(tax)
        loc = LocationSerializer().dump(loc)
        col = CollectorSerializer().dump(col)
        return {'id_exsiccate':data['id_exsiccate'],'taxonomy':tax,'location':loc,'collector':col}
    class Meta:
        model = Exsiccate
        ordered = True 
        sqla_session = Session