from abc import ABC, abstractmethod
from data_handles.eventdata.EventData import EventData


class EventsHandler(ABC):
    """Manage events to verify when and how files need to be scanned"""
    @abstractmethod
    def handle_event(self, event_data: EventData):
        """Log the event and send the scan request"""
        pass

    @abstractmethod
    def user_alert(self, event_data: EventData): 
        """Sends a notification to the user to inform the new event detection"""
        pass

    @abstractmethod
    def call_request(self, event_data: EventData):  
        """Call the component which manage the requests, log the results and inform the user of it"""
        pass
