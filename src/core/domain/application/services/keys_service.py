import rsa

from src.core.domain.application.services.Ikeys_service import IKeysService
from src.core.domain.models.keys_model import Keys
from src.adapters.drivens.infra.repositories.keys_repository import KeysRepository

class KeysService(IKeysService):
    def __init__(self):
        self.keys_repository = KeysRepository()
    
    @staticmethod
    def generate_key_pair()->tuple[rsa.PrivateKey,rsa.PublicKey]:
        """Generate an RSA key pair."""
        private_key, public_key = rsa.newkeys(2048)
        return private_key, public_key

    def save_keys(self):
        """Save user's key pair in the database."""
        private_key, public_key = self.generate_key_pair()
        
        keys = Keys(
            private_key=private_key.save_pkcs1().decode(),
            public_key=public_key.save_pkcs1().decode()
        )
        
        self.keys_repository.save_keys(keys)

    def get_keys(self, private_key:rsa.PrivateKey)->Keys:
        """Retrieve user's key pair."""
        keys = self.keys_repository.get_key(private_key)
        if not keys:
            raise ValueError("Keys not found for user")
        
        private_key = rsa.PrivateKey.load_pkcs1(keys.private_key.encode())
        public_key = rsa.PublicKey.load_pkcs1(keys.public_key.encode())
        return private_key, public_key