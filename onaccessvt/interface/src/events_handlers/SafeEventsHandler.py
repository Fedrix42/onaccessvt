from data_handles.eventdata.EventData import EventData
from events_handlers.EventsHandler import EventsHandler
from requests_handlers.VTRequestsHandler import RequestsHandler
from notifications.handlers.NTSendNotificationsHandler import NTSendNotificationsHandler
from notifications.Notification import Notification
from additionals.Logger import Logger
from data_handles.UrgencyType import UrgencyType
from additionals.messages import errors


class SafeEventsHandler(EventsHandler):
    def __init__(self, requestHandler: RequestsHandler, logger : Logger) -> None:
        self.requestHandler = requestHandler
        self.logger = logger
        self.verbose = False

    def handle_event(self, event_data: EventData) -> None:
        self.logger.log(event_data.to_log())
        self.call_request(event_data)

    def user_alert(self, event_data: EventData) -> None:
        if self.verbose:
            NTSendNotificationsHandler.notify(
                Notification(
                    event_data.format_notification_title(),
                    event_data.format_notification_body(),
                    UrgencyType.NORMAL,
                )
            )

    def call_request(self, file_data: EventData) -> None:
        """Get the result from the requestsHandler and inform the user if the file have some malicious entries
        or if verbose is true"""
        try:
            result = self.requestHandler.handle_request(file_data)
            self.logger.log(
                result.format_notification_title()
                + "\n"
                + result.format_notification_body()
            )
            if self.verbose or self.isResultPotentiallyHarmful(result):
                NTSendNotificationsHandler.notify(
                    Notification(
                        result.format_notification_title(),
                        result.format_notification_body(),
                        UrgencyType.NORMAL,
                    )
                )
        except Exception as e:
            #raise e #debug
            self.logger.log(
                errors.SCAN.format(file=file_data.entryName, e=e)
            )
            NTSendNotificationsHandler.notify(
                Notification(
                    errors.SCAN_TITLE,
                    errors.SCAN.format(
                        file=file_data.entryName, e=e
                    ),
                    UrgencyType.CRITICAL,
                )
            )

    def isResultPotentiallyHarmful(self, result) -> bool:
        """Check if the file have malicous entries"""
        if (
            int(result.vtobj.last_analysis_stats["malicious"]) > 0
            or int(result.vtobj.total_votes["malicious"]) > 0
        ):
            return True
        return False
    
