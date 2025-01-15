from dataclasses import dataclass

@dataclass
class TokenResult:
    user: str
    token: str
    expiration: str