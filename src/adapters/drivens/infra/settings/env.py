from dotenv import load_dotenv
import os

class ENV:

    def __init__(self):
        load_dotenv()
        self.DATABASE = os.getenv("DATABASE")
        self.SERVER_DB = os.getenv("SERVER_DB")
        self.PASSWORD_DB = os.getenv("PASSWORD_DB")
        self.USERNAME_DB = os.getenv("USERNAME_DB")
        self.CONNECT_STRING = os.getenv("CONNECT_STRING")
        self.PORT = os.getenv("PORT")
        self.SECRET_KEY_API = os.getenv("SECRET_KEY_API")