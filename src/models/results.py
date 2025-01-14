class TokenResult:
    def __init__(self, user: str, token: str, expiration: str):
        self.user = user
        self.token = token
        self.expiration = expiration