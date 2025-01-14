from datetime import datetime
from repository.bq_repository import BqRepository

class CSCService:
    def __init__(self):
        self.__db = BqRepository()

    def get_catalog_requests_csc(self):
        try:
            return self.__db.select_requests_csc()
        
        except Exception as ex:
            raise
    
    def get_requests_csc_status_from_user(self, user_email: str):
        try:
            return self.__db.select_requests_csc_status(user_email)
        
        except Exception as ex:
            raise