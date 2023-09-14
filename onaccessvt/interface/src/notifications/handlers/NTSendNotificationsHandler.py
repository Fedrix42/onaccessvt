import subprocess
from additionals import millis
from notifications.handlers.NotificationsHandler import NotificationsHandler
from notifications.Notification import Notification


class NTSendNotificationsHandler(NotificationsHandler):
    """Implementation of NotificationsHandler based on notify-send linux software"""
    notification_timeout = 1000  # milliseconds
    last_call = 0

    def notify(self, notification: Notification) -> None:
        """Send the notificaton when the user is ready"""
        while not self.isReady():
            pass
        self.send(notification)

    def send(self, notification: Notification) -> None:
        """Send the notification to the user"""
        exp_time_opt = str(NTSendNotificationsHandler.notification_timeout)
        subprocess.Popen(
            [
                "notify-send",
                "-u",
                str(notification.urgency.value),
                "-t",
                exp_time_opt,
                notification.__getattribute__("title"),
                notification.__getattribute__("body"),
            ]
        )
        self.last_call = millis.millis()

    def set_timeout(self, seconds : int):
        NTSendNotificationsHandler.notification_timeout  *= seconds


    def isReady(self) -> bool:
        """Check if the user is ready to receive a new notification(To avoid collisions)"""
        if (millis.millis() - self.last_call) < (
            NTSendNotificationsHandler.notification_timeout * 1.1
        ):
            return False
        else:
            return True
