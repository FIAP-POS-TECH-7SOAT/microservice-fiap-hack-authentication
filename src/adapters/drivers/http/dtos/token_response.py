from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class TokenResponse:
    payload: Dict[str,Any]
