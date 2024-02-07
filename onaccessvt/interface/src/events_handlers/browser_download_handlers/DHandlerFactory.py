from data_handles.eventdata.EventData import EventData
from data_handles.process_info.Browsers import Browsers
from events_handlers.browser_download_handlers.DHandler import DHandler
from events_handlers.browser_download_handlers.ChromeDHandler import ChromeDHandler
from events_handlers.browser_download_handlers.FirefoxDHandler import FirefoxDHandler

class DHandlerFactory():
    """Class Factory that returns the object that manages browser downloads"""

    @staticmethod
    def get_model(event_data : EventData) -> DHandler:
            match event_data.procinfo.processBrowser:
                  case Browsers.NOTFOUND:
                        return DHandler(event_data)
                  case Browsers.CHROME:
                        return ChromeDHandler(event_data)
                  case Browsers.FIREFOX:
                        return FirefoxDHandler(event_data)
            