from data_types.EventData import EventData
from events_handlers.EventsHandler import EventsHandler
from requests_handlers.VTRequestsHandler import RequestsHandler
from notifications.handlers.NTSendNotificationsHandler import NTSendNotificationsHandler
from notifications.Notification import Notification
from additionals.Logger import Logger
from data_types.UrgencyType import UrgencyType
from additionals.messages import errors


class SafeEventsHandler(EventsHandler):
    def __init__(self, requestHandler: RequestsHandler, logger : Logger) -> None:
        self.requestHandler = requestHandler
        self.notify_handler = NTSendNotificationsHandler()
        self.logger = logger
        self.verbose = False

    def handle_event(self, event_data: EventData) -> None:
        self.put_out_data(event_data)
        self.call_request(event_data)

    def put_out_data(self, event_data: EventData):
        """Log the event and notify the user of the event if verbose is true"""
        self.logger.log(event_data.to_log())
        if self.verbose:
            self.notify_handler.notify(
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
                self.notify_handler.notify(
                    Notification(
                        result.format_notification_title(),
                        result.format_notification_body(),
                        UrgencyType.NORMAL,
                    )
                )
        except Exception as e:
            #raise e #debug
            self.logger.log(
                errors.SCAN.format(file=file_data.__getattribute__("entryName"), e=e)
            )
            self.notify_handler.notify(
                Notification(
                    errors.SCAN_TITLE,
                    errors.SCAN.format(
                        file=file_data.__getattribute__("entryName"), e=e
                    ),
                    UrgencyType.CRITICAL,
                )
            )

    def isResultPotentiallyHarmful(self, result) -> bool:
        """Check if the file have malicous entries"""
        if (
            int(result.__getattribute__("vtobj").last_analysis_stats["malicious"]) > 0
            or int(result.__getattribute__("vtobj").total_votes["malicious"]) > 0
        ):
            return True
        return False

