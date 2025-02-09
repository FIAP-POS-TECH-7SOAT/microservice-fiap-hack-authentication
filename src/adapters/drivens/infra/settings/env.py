from dotenv import load_dotenv
import os

class ENV:

    def __init__(self):
        load_dotenv()
        self.CONNECT_STRING = os.getenv("CONNECT_STRING")
        self.PORT = os.getenv("PORT")
        self.EXP_DATE = os.getenv("EXP_DATE")
        self.PRIVATE_KEY = os.getenv("PRIVATE_KEY")
        self.PUBLIC_KEY = os.getenv("PUBLIC_KEY")
        self.BASE_URL = os.getenv("BASE_URL")
        self.SALT_KEY = os.getenv("SALT_KEY")
        self.EMAIL_HOST = os.getenv("EMAIL_HOST")
        self.EMAIL_PORT = int(os.getenv("EMAIL_PORT")) if os.getenv("EMAIL_PORT") else 587
        self.EMAIL_USER = os.getenv("EMAIL_USER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.EMAIL_FROM = os.getenv("EMAIL_FROM")
        self.EXP_SERIALIZER = int(os.getenv("EXP_SERIALIZER")) if os.getenv("EXP_SERIALIZER") else 86000