import time
from additionals.Logger import Logger
from data_handles.eventdata.EventData import EventData
from events_handlers.SafeEventsHandler import SafeEventsHandler
from requests_handlers.RequestsHandler import RequestsHandler
from data_handles.process_info.Browsers import Browsers
from events_handlers.browser_download_handlers.DHandlerFactory import DHandlerFactory
from events_handlers.browser_download_handlers.DHandler import DHandler


class BrowserEventsHandler(SafeEventsHandler):

    def __init__(self, rhandler: RequestsHandler, logger : Logger):
        super().__init__(rhandler, logger)
        

    def call_request(self, event_data: EventData) -> None:
        super().call_request(event_data)

    def handle_event(self, event_data: EventData) -> None:
        """Checks whenever the file is being downloaded by browser 
        and send a alert to the user to scan it after the download if finished"""
        if event_data.procinfo.processBrowser != Browsers.NOTFOUND:
            self.delay()
            downloadHandler : DHandler = DHandlerFactory.get_model(event_data)
            if downloadHandler.manage():
                super().handle_event(event_data)
        else:
            super().user_alert(event_data)
            super().handle_event(event_data)

    def delay(self):
        """This delay is useful because we need to wait the OS to update directory tree(So that behavioralModel can scan cwd)"""
        time.sleep(1)


