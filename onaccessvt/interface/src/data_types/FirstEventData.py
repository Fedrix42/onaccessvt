#!/usr/bin/python3
import hashlib
from pathlib import Path
import os
from data_types.RoughProcInfo import RoughProcInfo
from additionals.messages import infos, errors
from data_types.EventData import EventData


class FirstEventData(EventData):
    """First implementation of event data class"""
    SIZE_OF_EVENT_DATA = 8200
    READ_BUF_SIZE = 65536

    def __init__(self, buffered_data: bytes):
        """Read the bytes provided by argument and check if the length matches what expected, 
        then convert bytes into usable data type"""
        if len(buffered_data) != self.SIZE_OF_EVENT_DATA:
            raise Exception(errors.BUF_LEN)
        else:
            self.pid = int.from_bytes(buffered_data[0:4], byteorder="little") #PID of the process who created the file/event
            self.directoryPath = Path(
                (buffered_data[4:4100]).decode("UTF-8").rstrip("\x00")
            ) #Path of the directory where the file was created
            self.entryName = str((buffered_data[4100:8196]).decode("UTF-8")).rstrip("\x00"
            ) #Filename of the created file
            self.static_abs_path = Path(''.join([self.directoryPath.__str__(), '/', self.entryName])) #Static path of the file, it doesn't update
            self.inode = int.from_bytes(buffered_data[8196:8200], byteorder="little") #Inode useful if file has been renamed or moved
            self.procinfo = RoughProcInfo(self.pid)

    def get_dynamic_abs_path(self) -> Path:
        """
        This function tries to generate a dynamic path based on the inode.
        To do this it checks if there is a file in the original directory which has the same inode as the stored one.
        This is useful if the file has been renamed but not if it has been moved.
        """
        for file in os.listdir(self.directoryPath):
            current_path = ''.join([self.directoryPath.__str__(), '/', file])
            if os.stat(current_path).st_ino == self.inode:
                return Path(current_path)
        return self.static_abs_path
    

    def get_hash(self) -> str:
        """Calculate the hash of the file using hashlib"""
        sha1 = hashlib.sha1()
        if not self.entry_exists():
            raise RuntimeError(errors.ENTRY_NOT_EXISTS)
        
        with open(self.get_dynamic_abs_path(), "rb") as f:
            while True:
                """Read chunks of the file to better manage memory and big files"""
                data = f.read(FirstEventData.READ_BUF_SIZE)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()

    def entry_exists(self) -> bool:
        return self.get_dynamic_abs_path().exists()

    def to_log(self) -> str:
        """Format a string with event data for logging purpuse"""
        return infos.EVENT_DATA.format(
            pid=self.pid,
            dir=self.directoryPath,
            file=self.entryName,
            inode=self.inode,
            pname=self.procinfo.__getattribute__("process_name"),
        )

    def format_notification_title(self) -> str:
        """Format a string with event data for notification purpuse"""
        return infos.NEW_EVENT

    def format_notification_body(self) -> str:
        """Format a string with event data for notification purpuse"""
        return infos.NOTI_EVENT_DATA_BODY.format(abs=self.absolutePath)
