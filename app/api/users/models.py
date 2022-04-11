from api.factory import db_instance as db
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
class User(db.Model):
    user_id = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid4,unique=True)
    user_name = db.Column(db.String(80))
    user_mail = db.Column(db.String(80))
    user_password = db.Column(db.String(80))
    user_foundation = db.Column(db.String(80))
    def save(self):
        db.session.add(self)
        return db.session.commit()
    def committed(self):
        return db.session.commit()
    def destroy(self):
        db.session.delete(self)
        return db.session.commit()
