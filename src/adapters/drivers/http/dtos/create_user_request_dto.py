from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    user_email: str
    password: str
    phone:str
