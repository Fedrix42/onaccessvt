from datetime import datetime, date
import os
from additionals.messages.infos import LOG_HEADER,LOG_FOOTER

class Logger:
    LOG_DIRECTORY="/var/log/onaccessvt/interface"
    DATA_FORMAT = '%d %b %Y, %H:%M:%S'

    def log(self, str : str) -> None:
        """Check if a log file of today already exists, if it does than it is used.
        Otherwise a new log file is created"""
        path = self.get_log_file() 
        if path != None:
            f = open(path, "a")
            self.write_to_file(f, str)
        else:
            f = open(self.get_now_full_path(), "w")
            self.write_to_file(f, str)
        f.close()

    def write_to_file(self, file, str : str) -> None:
        """Write message contained in str to log file with a header and a footer"""
        file.write(LOG_HEADER.format(date=datetime.now().__str__()))
        file.write(str)
        file.write(LOG_FOOTER)


    def get_log_file(self):
        """Check if there is already a log file created today"""
        filesInCWD = [f for f in os.listdir(Logger.LOG_DIRECTORY)]
        for file in filesInCWD:
            try:
                if datetime.strptime(file, Logger.DATA_FORMAT).date() == date.today():
                    return os.path.join(Logger.LOG_DIRECTORY, file)
            except ValueError:
                pass
        return None
    
    def get_now_full_path(self):
        return os.path.join(Logger.LOG_DIRECTORY, datetime.now().strftime(Logger.DATA_FORMAT))
