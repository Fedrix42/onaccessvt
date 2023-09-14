USAGE = """\
Usage: {argv} [-v] -a (api-key) -dt (download_timeout) -nt(notifications_timeout) [fifo_path]
    -> -v, verbose: Optional, if set show a notification for every event detected even if they have 0 malicious entries
    -> -a, api-key: is the API key from virus total website(account required)
    -> -dt, download_timeout: is the timeout, expressed in MINUTES, that the process will wait for the completion of big file downloads
    -> -nt, notifications_timeout: is the timeout, expressed in SECONDS, for notifications
Check documentation for more info...
"""
START = "This program should be run only when event monitor is already running.\nOpening FIFO..."
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
LOG_HEADER="--Start of log: {date}--\n"
LOG_FOOTER="\n--End of log--\n"

