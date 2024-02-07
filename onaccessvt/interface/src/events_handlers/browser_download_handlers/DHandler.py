from abc import ABC, abstractmethod

class DHandler(ABC):
    """This astract class manages browser downloads. 
    When the download behavior of browsers changes the subclasses have to be updated!"""

    @abstractmethod
    def downloading(self) -> bool:
        """Return true if the file is being downloaded by the browser"""
        pass

    @abstractmethod
    def manage(self) -> bool:
        """Manage the browser download, return true if the event requires a scan or false alternatively"""
        pass