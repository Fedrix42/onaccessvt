from abc import ABC, abstractmethod
from data_handles.eventdata.EventData import EventData

class BehavioralModel(ABC):
    """This astract class checks if a download matches the behavior of a browser"""

    @abstractmethod
    def behavior_matches(self, event_data : EventData) -> bool:
        """Return true if the file is being downloaded by a certain browser"""
        pass