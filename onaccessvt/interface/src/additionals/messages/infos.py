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
DIAL_BOX_TITLE="OnAccessVT - User action required"
DIAL_BOX_BODY="File: {file} is being downloaded by a browser.\nIf you want to scan it, press 'YES' ONLY when the download is finished"
LOG_HEADER="\n=====   {date}   =====\n"
LOG_FOOTER="\n==========================================\n"

