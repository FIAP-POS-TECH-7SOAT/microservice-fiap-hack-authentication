from abc import ABC, abstractmethod

import rsa

from src.core.domain.models.keys_model import Keys

class IKeysRepository(ABC):
    
    @abstractmethod
    def save_keys(self, keys:Keys):
        pass
    
    @abstractmethod
    def get_key(self, private_key:rsa.PrivateKey)->Keys:
        pass
    
    @abstractmethod
    def delete_key(self, private_key:str):
        pass