import os
from browser_download_handlers.BehavioralModel import BehavioralModel
from data_handles.eventdata.EventData import EventData

class FirefoxBehavioralModel(BehavioralModel):
    def behavior_matches(self, event_data: EventData) -> bool:
        """Check if the file is being downloaded by a chrome browser using file extensions"""
        if event_data.entryName.endswith("crdownload"):
            return True
        return False