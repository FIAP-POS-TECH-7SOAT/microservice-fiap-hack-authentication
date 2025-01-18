from src.adapters.drivens.infra.database.config import db

class Keys(db.Model):
    __tablename__ = 'keys'
    private_key = db.Column(db.String, primary_key=True)
    public_key = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.Datetime, nullable=False)
    active = db.Column(db.Bool, nullable=False)