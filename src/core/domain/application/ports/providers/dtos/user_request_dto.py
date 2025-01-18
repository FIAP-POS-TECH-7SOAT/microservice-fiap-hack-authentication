from dataclasses import dataclass

@dataclass
class UserRequest:
    user_email: str
    password: str
