import os
import time
import tkinter.messagebox
from additionals import millis
from additionals.messages import infos
from data_types.EventData import EventData
from events_handlers.EventsHandler import EventsHandler
from requests_handlers.RequestsHandler import RequestsHandler


class BrowserEventsHandler(EventsHandler):

    def __init__(self, rhandler: RequestsHandler):
        super().__init__(rhandler)

    def call_request(self, event_data: EventData) -> None:
        super().call_request(event_data)

    def handle_event(self, event_data: EventData) -> None:
        if event_data.__getattribute__('procinfo').__getattribute__("isABrowser"):
            time.sleep(1)
            if self.is_download_in_process(event_data):
                if tkinter.messagebox.askyesno(infos.DIAL_BOX_TITLE, infos.DIAL_BOX_BODY.format(file=event_data.__getattribute__("entryName"))):
                    super().handle_event(event_data)
            else:
                super().handle_event(event_data)
        else:
            super().handle_event(event_data)

    def is_download_in_process(self, event_data: EventData) -> bool:
        return self.firefox_check(event_data) or self.chrome_check(event_data)

    def firefox_check(self, event_data: EventData):
        filename = event_data.__getattribute__("entryName")
        entriesInCWD = [f for f in os.listdir(event_data.__getattribute__('directoryPath'))]
        for entry in entriesInCWD:
            if entry.startswith(filename.split(".")[0]) and entry.endswith(".part"):
                return True
        return False

    def chrome_check(self, event_data : EventData):
        if event_data.__getattribute__("entryName").endswith("crdownload"):
            return True
        return False

