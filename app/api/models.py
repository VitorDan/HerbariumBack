# from sqlalchemy.sql.sqltypes import String
from api.factory import db_instance as db
from sqlalchemy.dialects.postgresql import BIGINT as BigInt
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4



images_association = db.Table('images_association', db.Model.metadata,
    db.Column('exsiccate_id', UUID(as_uuid=True), db.ForeignKey('exsiccate.id_exsiccate')),
    db.Column('image_id', UUID(as_uuid=True), db.ForeignKey('image.id_image'))
)


class Taxonomy(db.Model):
    __tablename__ = 'taxonomy'
    id_taxonomy = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4,unique=True)
    kingdom = db.Column(db.String(80))
    phylum = db.Column(db.String(80))
    e_class = db.Column(db.String(80))
    order = db.Column(db.String(80))
    family = db.Column(db.String(80))
    genus = db.Column(db.String(80))
    specific_epithet = db.Column(db.String(80))
    #Relation 
    exsiccate = db.relationship("Exsiccate",cascade='all,delete', uselist=False, back_populates='taxon', lazy = "select")
    def save(self):
        db.session.add(self)
        return db.session.commit()
    def committed(self):
        return db.session.commit()
    def destroy(self):
        db.session.delete(self)
        return db.session.commit()
class Collector(db.Model):
    __tablename__ = 'collector'
    id_collector = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4,unique=True)
    collector_name = db.Column(db.String(80))
    collector_mail = db.Column(db.String(80))
    collector_password = db.Column(db.String(80))
    collector_office = db.Column(db.Boolean)
    collector_foundation = db.Column(db.String(80))
    collector_cite = db.Column(db.String(12))
    collector_birthday = db.Column(db.Date())
    #Relation
    exsiccate = db.relationship("Exsiccate",cascade='all,delete', uselist=False, back_populates='col',lazy = "select")
    def save(self):
        db.session.add(self)
        return db.session.commit()
    def committed(self):
        return db.session.commit()
    def destroy(self):
        db.session.delete(self)
        return db.session.commit()
class Location (db.Model):
    __tablename__ = 'location'
    id_location = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4,unique=False)
    country = db.Column(db.String(80))
    stateprovince = db.Column(db.String(80))
    city = db.Column(db.String(80))
    county = db.Column(db.String(80))
    latitude = db.Column(BigInt)
    longitude = db.Column(BigInt)
    elevation = db.Column(db.Integer())
    #Relation
    exsiccate = db.relationship("Exsiccate",cascade='all,delete', uselist=False,back_populates="loco",lazy = "select")
    def save(self):
        db.session.add(self)
        return db.session.commit()
    def committed(self):
        return db.session.commit()
    def destroy(self):
        db.session.delete(self)
        return db.session.commit()
class Exsiccate(db.Model):
    __tablename__= 'exsiccate'
    id_exsiccate = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4,unique=True)
    id_taxonomy = db.Column(UUID(as_uuid=True), db.ForeignKey('taxonomy.id_taxonomy'))
    id_location = db.Column(UUID(as_uuid=True), db.ForeignKey('location.id_location'))
    id_collector = db.Column(UUID(as_uuid=True), db.ForeignKey('collector.id_collector'))
    taxon = db.relationship('Taxonomy', cascade="all,delete",uselist=False,back_populates='exsiccate',lazy = "select")
    loco = db.relationship('Location', cascade="all,delete",uselist=False, back_populates='exsiccate',lazy = "select")
    col = db.relationship('Collector',cascade="all,delete",back_populates='exsiccate',lazy = "select")
    images = db.relationship('Image',cascade="all,delete",secondary=images_association,backref=db.backref('exsiccate', lazy=True))
    def save(self):
        db.session.add(self)
        return db.session.commit()
    def committed(self):
        return db.session.commit()
    def destroy(self):
        db.session.delete(self)
        return db.session.commit()
class Image(db.Model):
    __tablename__= 'image'
    id_image = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4,unique=True)
    image_extension = db.Column(db.String(3))
    def save(self):
        db.session.add(self)
        return db.session.commit()
    def committed(self):
        return db.session.commit()
    def destroy(self):
        db.session.delete(self)
        return db.session.commit()