import subprocess
from additionals import millis
from notifications.handlers.NotificationsHandler import NotificationsHandler
from notifications.Notification import Notification


class NTSendNotificationsHandler(NotificationsHandler):
    """Implementation of NotificationsHandler based on notify-send linux software"""
    notification_timeout = 5000  # milliseconds
    last_call = 0

    def notify(notification: Notification) -> None:
        """Send the notificaton when the user is ready"""
        while not NTSendNotificationsHandler.isReady():
            pass
        NTSendNotificationsHandler.send(notification)

    def send(notification: Notification) -> None:
        """Send the notification to the user"""
        exp_time_opt = str(NTSendNotificationsHandler.notification_timeout)
        subprocess.Popen(
            [
                "notify-send",
                "-u",
                str(notification.urgency.value),
                "-t",
                exp_time_opt,
                notification.title,
                notification.body,
            ]
        )
        NTSendNotificationsHandler.last_call = millis.millis()


    def isReady() -> bool:
        """Check if the user is ready to receive a new notification(To avoid collisions)"""
        if (millis.millis() - NTSendNotificationsHandler.last_call) < (
            NTSendNotificationsHandler.notification_timeout * 1.1
        ):
            return False
        else:
            return True
