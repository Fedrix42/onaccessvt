from abc import ABC, abstractmethod


class NotificationsHandler(ABC):
    """Abstract class to send notifications to the user"""
    @abstractmethod
    def notify(self):
        pass
