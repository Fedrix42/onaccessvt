from data_types.UrgencyType import UrgencyType


class Notification:
    """Holds information of a notification(based on linux notification system)"""
    def __init__(self, title: str, body: str, urgency: UrgencyType):
        self.title = title
        self.body = body
        self.urgency = urgency
