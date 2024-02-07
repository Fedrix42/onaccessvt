from events_handlers.browser_download_handlers.DHandler import DHandler
from data_handles.eventdata.EventData import EventData
from notifications.handlers.NTSendNotificationsHandler import NTSendNotificationsHandler
from notifications.Notification import Notification
from additionals.messages import infos
from data_handles.UrgencyType import UrgencyType

class ChromeDHandler(DHandler):
    temp_files_keywords = {"crdownload", ".com.google", ".com", "Chrome"}

    def __init__(self, event_data : EventData):
        self.event_data = event_data

    def downloading(self) -> bool:
        """Check if the file is being downloaded by a chrome browser using file extensions"""
        for keyword in ChromeDHandler.temp_files_keywords:
            if keyword in self.event_data.entryName:
                return True
        return False

    def manage(self) -> bool:
        if self.downloading():
            NTSendNotificationsHandler.notify(Notification(
                    infos.DOWNLOAD_WAITING_TITLE.format(bname="Chrome"),
                    infos.DOWNLOAD_WAITING_BODY,
                    UrgencyType.NORMAL)
                )
            return False
        return True