from datetime import datetime
from configs.app_settings import AppSettings
from sqlalchemy import create_engine, text

class TokenRepository:
    def __init__(self):
        self.engine = create_engine(AppSettings.CONNECT_STRING)
        self.connection = self.engine.connect()

    def insert_refresh_token(self, session_id: str, user_email: str, access_token: str, refresh_token: str, expires_at: datetime):
        try:
            query = f"DELETE FROM REFRESH_TOKENS WHERE USER_ID = '{user_email}'"
            self.connection.execute(text(query))

            query = f"""INSERT INTO REFRESH_TOKENS(SESSION_ID, USER_ID, ACCESS_TOKEN, REFRESH_TOKEN, 
            EXPIRES_AT) VALUES ('{session_id}', '{user_email}', '{access_token}', '{refresh_token}', '{expires_at}')"""
            self.connection.execute(text(query))

            query = f"""INSERT INTO TRACK_USER_ACCESS(USER_ID) VALUES ('{user_email}')"""
            self.connection.execute(text(query))

            self.connection.commit()
            self.close_connection()

        except Exception as e:
            raise

    def get_refresh_token(self, user_email: str):
        try:

            query = f"""SELECT SESSION_ID, ACCESS_TOKEN, REFRESH_TOKEN, 
                EXPIRES_AT FROM REFRESH_TOKENS WHERE USER_ID = '{user_email}'"""
            result = self.__execute_query(query)
            
            self.close_connection()

            return result
        
        except Exception as e:
            raise

    def update_access_token_from_session_id(self, session_id: str, access_token: str):
        try:
            connection = self.engine.connect()

            query = f"""UPDATE REFRESH_TOKENS 
                SET ACCESS_TOKEN = '{access_token}' 
                WHERE SESSION_ID = '{session_id}'"""
            
            connection.execute(text(query))
            connection.commit()
            connection.close()
        
        except Exception as e:
            raise

    def __execute_query(self, query):
        try:
            
            result = self.connection.execute(text(query))
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        
        except Exception as e:
            raise

    def close_connection(self):
        try:
            self.connection.close()
            self.engine.dispose()

        except Exception as e:
            print(e)