import psutil
from re import search
from data_handles.process_info.ProcInfo import ProcInfo
from data_handles.process_info.Browsers import Browsers


class PSUtilProcInfo(ProcInfo):
    BROWSER_NAMES = [
        {"chrome", "chromium", "xdg-document-portal", "xdg"},
        {"firefox", "mozilla"}
    ]

    def __init__(self, pid: int):
        try:
            self.process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            self.process = psutil.Process(1)
        self.pid = self.process.pid
        self.process_name = self.process.name()
        self.process_cmdline = self.process.cmdline()
        self.processBrowser = Browsers(self.is_process_a_browser())


    def search_in_cmdline(self, keyword : str, cmdline : list) -> bool:
        for x in cmdline:
            if search(keyword, x):
                return True
        return False

    def search_in_process(self, keyword : str) -> bool:
        try:
            parent = self.process.parent()
        except psutil.NoSuchProcess:
            parent = None
        
        if search(keyword, self.process_name) or self.search_in_cmdline(keyword, self.process_cmdline) :
            return True
        elif type(parent) == psutil.Process:
            if search(keyword, parent.name()) or self.search_in_cmdline(keyword, parent.cmdline()):
                return True
        
        return False


    def is_process_a_browser(self) -> int:
        """Determines if the process is a browser by checking if there is a word of the dictionary
        above in the process name and cmdline and in the process parent name and cmdline
        """
        for browser in PSUtilProcInfo.BROWSER_NAMES:
            for browser_keyword in browser:
                if self.search_in_process(browser_keyword):
                    return PSUtilProcInfo.BROWSER_NAMES.index(browser)
        return -1
