import os
from browser_download_handlers.BehavioralModel import BehavioralModel
from data_handles.eventdata.EventData import EventData

class FirefoxBehavioralModel(BehavioralModel):
    def behavior_matches(self, event_data: EventData) -> bool:
        """Check if the file is being downloaded by a firefox browser.
        Searches for a .part file on the same directory of the event file"""
        filename = event_data.entryName
        entriesInCWD = [f for f in os.listdir(event_data.directoryPath)]
        for entry in entriesInCWD:
            if entry.startswith(filename.split(".")[0]) and entry.endswith(".part"):
                return True
        return False