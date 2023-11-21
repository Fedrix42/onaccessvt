import vt
from data_handles.eventdata.EventData import EventData
from additionals.messages import infos


class ScanResult:
    """Holds informations of a successfully executed scan for a specific event"""

    def __init__(self, event_data: EventData, vtobj: vt.Object) -> None:
        self.event_data = event_data
        self.vtobj = vtobj

    def format_notification_title(self) -> str:
        """Format a string with scan results data for notification purpuse"""
        return infos.NOTI_SCAN_RES_TITLE

    def format_notification_body(self) -> str:
        """Format a string with scan results data for notification purpuse"""
        return infos.NOTI_SCAN_RES_BODY.format(
            file=self.event_data.static_abs_path,
            malicious=self.vtobj.last_analysis_stats["malicious"],
            undetected=self.vtobj.last_analysis_stats["undetected"],
            harmless=self.vtobj.last_analysis_stats["harmless"],
            votes_harmless=self.vtobj.total_votes["harmless"],
            votes_malicious=self.vtobj.total_votes["malicious"],
        )
