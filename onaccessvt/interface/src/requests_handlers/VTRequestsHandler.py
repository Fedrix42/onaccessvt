#!/usr/bin/python3
from data_types.EventData import EventData
import vt
from requests_handlers.RequestsHandler import RequestsHandler
from requests_handlers.ScanResult import ScanResult


class VTRequestsHandler(RequestsHandler):
    """RequestsHandler implementing VirusTotal API"""
    BUF_SIZE = 65536

    def __init__(self, APIKey: str):
        self.setAPIKey(APIKey)

    def __init__(self):
        self.client = None

    def setAPIKey(self, APIKey: str) -> None:
        """Set the API key for the VirusTotal API and check if it's valid by executing a hash submit scan"""
        self.client = vt.Client(APIKey)
        self.client.get_object("/files/f5b29a273cd9f03f90b8c5f471e937c82fd703c2")

    def handle_request(self, event_data: EventData) -> ScanResult:
        """Currently supporting only hash based scan"""
        vtobj = self.hash_submit(event_data.get_hash())
        return ScanResult(event_data, vtobj)


    def hash_submit(self, hash: str) -> vt.Object:
        return self.client.get_object(f"/files/{str(hash)}")

    def getClient(self):
        return self.client
