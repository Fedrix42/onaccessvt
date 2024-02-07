import os
import time
from data_handles.UrgencyType import UrgencyType
from events_handlers.browser_download_handlers.DHandler import DHandler
from notifications.handlers.NTSendNotificationsHandler import NTSendNotificationsHandler
from notifications.Notification import Notification
from additionals.messages import infos
from data_handles.eventdata.EventData import EventData

class FirefoxDHandler(DHandler):

    def __init__(self, event_data : EventData):
        self.event_data = event_data

    def downloading(self) -> bool:
        """Searches for a .part file on the same directory of the event file"""
        filename = self.event_data.entryName
        entriesInCWD = [f for f in os.listdir(self.event_data.directoryPath)]
        for entry in entriesInCWD:
            if entry.startswith(filename.split(".")[0]) and entry.endswith(".part"):
                return True
        return False
    
    def manage(self) -> bool:
        if self.downloading():
            NTSendNotificationsHandler.notify(Notification(
                    infos.DOWNLOAD_WAITING_TITLE.format(bname="Firefox"),
                    infos.DOWNLOAD_WAITING_BODY,
                    UrgencyType.NORMAL)
                )
        while self.downloading():
            time.sleep(3)
        return True