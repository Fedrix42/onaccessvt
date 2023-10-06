import os
import time
import tkinter.messagebox
from additionals.messages import infos
from additionals.Logger import Logger
from data_types.EventData import EventData
from events_handlers.SafeEventsHandler import SafeEventsHandler
from requests_handlers.RequestsHandler import RequestsHandler


class BrowserEventsHandler(SafeEventsHandler):

    def __init__(self, rhandler: RequestsHandler, logger : Logger):
        super().__init__(rhandler, logger)

    def call_request(self, event_data: EventData) -> None:
        super().call_request(event_data)

    def handle_event(self, event_data: EventData) -> None:
        """Checks whenever the file is being downloaded by browser 
        and send a alert to the user to scan it after the download if finished"""

        if event_data.__getattribute__('procinfo').__getattribute__("isABrowser"):
            time.sleep(1) 
            """This delay is helpful because some browsers create a .part file 
            and some time passes between this code executed and the creation of the .part file"""
            if self.is_download_in_process(event_data):
                if tkinter.messagebox.askyesno(infos.DIAL_BOX_TITLE, infos.DIAL_BOX_BODY.format(file=event_data.__getattribute__("entryName"))):
                    super().handle_event(event_data)
            else:
                super().handle_event(event_data)
        else:
            super().handle_event(event_data)

    def is_download_in_process(self, event_data: EventData) -> bool:
        """Check if file is being downloaded by different browsers based on their behaviour.
        I should find a way to do this that is the same for all browsers."""
        return self.firefox_check(event_data) or self.chrome_check(event_data)

    def firefox_check(self, event_data: EventData):
        """Check if the file is being downloaded by a firefox browser.
        Searches for a .part file on the same directory of the event file"""
        filename = event_data.__getattribute__("entryName")
        entriesInCWD = [f for f in os.listdir(event_data.__getattribute__('directoryPath'))]
        for entry in entriesInCWD:
            if entry.startswith(filename.split(".")[0]) and entry.endswith(".part"):
                return True
        return False

    def chrome_check(self, event_data : EventData):
        """Check if the file is being downloaded by a chrome browser."""
        if event_data.__getattribute__("entryName").endswith("crdownload"):
            return True
        return False

