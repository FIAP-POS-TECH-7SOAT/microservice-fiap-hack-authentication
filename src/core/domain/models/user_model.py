from datetime import datetime
from uuid import uuid4

from src.adapters.drivens.infra.database.config import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=uuid4())
    user_email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    registered_at = db.Column(db.Datetime, nullable=True, default=datetime.now())
    active = db.Column(db.Bool, nullable=True, default=True)