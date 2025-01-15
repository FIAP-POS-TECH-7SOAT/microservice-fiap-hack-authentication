from src.adapters.drivens.infra.database.config import db

class Token(db.Model):
    __tablename__ = 'REFRESH_TOKENS'
    session_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)