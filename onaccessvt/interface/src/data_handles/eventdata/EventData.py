from abc import ABC, abstractmethod


class EventData(ABC):
    """Abstract class to hold informations about the file that was created and the process who
    created it. Also do convert the bytes read in the fifo to usable data types."""

    @abstractmethod
    def get_hash(self):
        """Get the file hash(sha1) of the created file"""
        pass


    @abstractmethod
    def entry_exists(self):
        """Check if the file exists at call time"""
        pass
