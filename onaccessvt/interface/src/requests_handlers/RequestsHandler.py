from abc import ABC, abstractmethod
import data_handles.eventdata.EventData as EventData
import vt


class RequestsHandler(ABC):
    """This abstract class handles the HTTP requests to a malware scanning platform
    To Do:
        -file_submit for upload
        -url scan
    """
    @abstractmethod
    def handle_request(self, event_data: EventData):
        """Handle the request"""
        pass

    @abstractmethod
    def hash_submit(self, hash: str):
        """This method should handle the request of a scan based on a provided file hash"""
        pass


