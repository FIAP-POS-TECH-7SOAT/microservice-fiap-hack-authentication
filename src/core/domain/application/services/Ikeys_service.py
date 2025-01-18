from abc import ABC, abstractmethod

import rsa

from src.core.domain.models.keys_model import Keys

class IKeysService(ABC):
    @abstractmethod
    def generate_key_pair()->tuple[rsa.PrivateKey,rsa.PublicKey]:
        """Generate an RSA key pair."""
        pass
    
    @abstractmethod
    def save_keys(self):
        """Save user's key pair in the database."""
        pass

    @abstractmethod
    def get_keys(self, private_key:rsa.PrivateKey)->Keys:
        """Retrieve user's key pair."""
        pass