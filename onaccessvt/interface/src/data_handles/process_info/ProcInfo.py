from abc import ABC, abstractmethod


class ProcInfo(ABC):
    """Abstract class to manage informations about the process who created the event"""

    @abstractmethod
    def is_process_a_browser(self):
        """Check if the process can be considerated as a browser, useful for handle file downloading"""
        pass
