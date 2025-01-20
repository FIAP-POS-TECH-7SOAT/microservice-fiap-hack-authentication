from src.core.domain.application.ports.repositories.Ikeys_repository import IKeysRepository
from src.adapters.drivens.infra.database.config import db
from src.core.domain.models.keys_model import Keys

import rsa

from sqlalchemy.exc import SQLAlchemyError

class KeysRepository(IKeysRepository):
    def __init__(self):
        self.db = db
        
    def save_keys(self, keys:Keys):
        try:
            self.db.session.add(keys)
            self.db.session.commit()
            
        except SQLAlchemyError as e:
            print(e)
            self.db.session.rollback()
            raise

    def get_key_by_private_key(self, private_key:rsa.PrivateKey)->Keys:
        try:
            return Keys.query.filter_by(private_key=private_key).first()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise
        
    def get_key(self)->Keys:
        try:
            return Keys.query.filter(Keys.active == True).first()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise
        
    def delete_key(self, private_key:str):
        try:
            key = self.get_key_by_private_key(private_key)
            if key:
                key.active = False
                self.db.session.commit()
        
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise