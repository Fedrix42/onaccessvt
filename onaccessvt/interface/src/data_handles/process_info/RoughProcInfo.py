import subprocess
from re import search
from data_handles.process_info.ProcInfo import ProcInfo


class RoughProcInfo(ProcInfo):
    BROWSER_NAMES = [
        "firefox",
        "chrome",
        "brave",
        "bwrap"
    ]

    def __init__(self, pid: int):
        self.pid = pid
        self.process_name = self.get_pname()
        self.isABrowser = self.is_process_a_browser()

    def get_pname(self) -> str:
        """Get the process name using the linux cmd ps and specifying the PID"""
        p = subprocess.Popen(
            ["ps -o cmd= {}".format(self.pid)], stdout=subprocess.PIPE, shell=True
        )
        return (p.communicate()[0].decode("UTF-8")).rstrip("\n")

    def is_process_a_browser(self) -> bool:
        """Determines if the process is a browser by checking if there is a word of the dictionary
        above in the process name(I now it isn't accurate, future-proof or anything good)
        To Do:
            -throw into trashbin this and find a better way to do the job
        """
        for browser_name in RoughProcInfo.BROWSER_NAMES:
            if search(browser_name, self.process_name):
                return True
        return False
