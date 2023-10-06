from abc import ABC, abstractmethod
from data_types.EventData import EventData


class EventsHandler(ABC):
    """Manage events to verify when and how files need to be scanned"""
    @abstractmethod
    def handle_event(
        self, event_data: EventData
    ):  
        pass

    @abstractmethod
    def put_out_data(self, event_data: EventData): 
        """Sends data to appropiate components to log them or to inform the user"""
        pass

    @abstractmethod
    def call_request(self, event_data: EventData):  
        """Call the component which manage the requests, log the results and inform the user of it"""
        pass
