from dataclasses import dataclass

@dataclass
class AuthUser:
    user_email: str
    password: str
