import os

class AppSettings:
    CONNECT_STRING = os.getenv("CONNECT_STRING")
    SECRET_KEY_API = os.getenv("SECRET_KEY_API")
    URL_FINANCE_GATEWAY = os.getenv("URL_FINANCE_GATEWAY")
    OAUTH_URL = os.getenv("OAUTH_URL")
    OAUTH_GRANT_TYPE = os.getenv("OAUTH_GRANT_TYPE")
    OAUTH_USER_INFO = os.getenv("OAUTH_USER_INFO")
    OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")
    OAUTH_REDIRECT_URL = os.getenv("OAUTH_REDIRECT_URL")
