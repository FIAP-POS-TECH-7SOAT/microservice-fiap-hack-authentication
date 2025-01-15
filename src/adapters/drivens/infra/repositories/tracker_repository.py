from src.core.domain.application.ports.repositories.Itracker_repository import ITrackerRepository
from src.core.domain.models.tracker_model import TrackUserAccess
from src.adapters.drivens.infra.database.config import db

from sqlalchemy.exc import SQLAlchemyError

class TrackerRepository(ITrackerRepository):
    def __init__(self):
        self.db = db
        
    def save_tracker(self, track_access:TrackUserAccess):
        try:
            self.db.session.add(track_access)
            self.db.session.commit()
            
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise