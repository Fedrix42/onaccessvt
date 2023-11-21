from additionals.messages import errors

"""This module do conversion from bytes to usable data type for EventData costructor"""

SIZE_OF_EVENT_DATA = 8200
R = { #Ranges of data
    'pid' : (0, 4),
    'dirpath' : (4, 4100),
    'entryname' : (4100, 8196),
    'inode' : (8196, 8200),
}

def check_received_bytes_length(raw_data: bytes):
    if len(raw_data) != SIZE_OF_EVENT_DATA:
        raise Exception(errors.BUF_LEN)

def extract_pid(buffered_data: bytes) -> int:
    pid = int.from_bytes(buffered_data[R['pid'][0]:R['pid'][1]], byteorder="little") #PID of the process who created the file/event
    return pid

def extract_directory(buffered_data: bytes) -> str:
    directoryPath = (buffered_data[R['dirpath'][0]:R['dirpath'][1]]).decode("UTF-8").rstrip("\x00") #Str of path of the directory where the file was created
    return directoryPath
    
def extract_entryName(buffered_data: bytes) -> str:
    entryName = str((buffered_data[R['entryname'][0]:R['entryname'][1]]).decode("UTF-8")).rstrip("\x00") #Str of filename of the created file
    return entryName

def extract_inode(buffered_data: bytes) -> int:
    inode = int.from_bytes(buffered_data[R['inode'][0]:R['inode'][1]], byteorder="little") #Inode useful if file has been renamed or moved
    return inode