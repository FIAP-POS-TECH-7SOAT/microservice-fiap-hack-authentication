from datetime import datetime
from src.adapters.drivens.infra.database.config import db

class Keys(db.Model):
    __tablename__ = 'keys'
    private_key = db.Column(db.String, primary_key=True)
    public_key = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    active = db.Column(db.Boolean, nullable=False, default=True)