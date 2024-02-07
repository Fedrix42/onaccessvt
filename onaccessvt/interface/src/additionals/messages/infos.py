START = "Program started, it should run only when event monitor is already running.\nOpening FIFO..."
EVENT_DATA = (
    "PID: {pid}\nDirectory path: {dir}\nEntry name: {file}\nInode: {inode}\nProcess name: {pname}\n"
)
NEW_EVENT = "OnAccessVT - New event detected"
NOTI_EVENT_DATA_BODY = "File path: {abs}\n"
NOTI_SCAN_RES_TITLE = "OnAccessVT - SCAN RESULTS"
NOTI_SCAN_RES_BODY = """\
File:{file}
     Malicious -> {malicious}
     Undetected -> {undetected}
     Harmless -> {harmless}
Community votes(Harmless -> {votes_harmless} || Malicious -> {votes_malicious})
"""
DOWNLOAD_WAITING_TITLE="OnAccessVT - {bname} download detected" #Browser name
DOWNLOAD_WAITING_BODY="The download of a file was detected.\nIt will be scanned when the download ends."
LOG_HEADER="\n=====   {date}   =====\n"
LOG_FOOTER="\n==========================================\n"

