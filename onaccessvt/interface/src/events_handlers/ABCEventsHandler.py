from abc import ABC, abstractmethod
from data_types.EventData import EventData


class ABCEventsHandler(ABC):
    @abstractmethod
    def handle_event(
        self, event_data: EventData
    ):  
        pass

    @abstractmethod
    def put_out_data(self, event_data: EventData): # print event data or log it
        pass

    @abstractmethod
    def call_request(self, event_data: EventData):  # call vt api for scan of a file
        pass
