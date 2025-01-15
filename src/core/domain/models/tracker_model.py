from src.adapters.drivens.infra.database.config import db
from datetime import datetime

class TrackUserAccess(db.Model):
    __tablename__ = 'TRACK_USER_ACCESS'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)