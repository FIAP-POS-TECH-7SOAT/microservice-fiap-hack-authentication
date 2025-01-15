from abc import ABC, abstractmethod

class ITrackerRepository(ABC):
    @abstractmethod
    def save_tracker(self, user_id:str):
        """Save tracker into Database"""
        pass