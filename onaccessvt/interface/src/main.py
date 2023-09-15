#!/usr/bin/python3
from data_types.FirstEventData import FirstEventData
from additionals.messages import infos, errors
from additionals.Logger import Logger
from requests_handlers.VTRequestsHandler import VTRequestsHandler
from events_handlers.BrowserEventsHandler import BrowserEventsHandler
import os
import sys
import signal

import argparse

FIFO_PATH = "/tmp/on_accessvt_fifo"
requestsHandler = VTRequestsHandler()
logger = Logger()
browserEventsHandler = BrowserEventsHandler(requestsHandler, logger)



def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGPIPE, signal_handler)
    check_argv()
    read_from_fifo()


def read_from_fifo():
    """Read from named pipe/fifo and print any exceptions
    Exceptions that reach this function should be related to bad arguments or critical errors that occur
    only when the program start
    """
    global requestsHandler
    global browserEventsHandler
    print(infos.START)
    try:
        with open(FIFO_PATH, "rb") as fifo:
            print("FIFO opened")
            while True:
                data = fifo.read(FirstEventData.SIZE_OF_EVENT_DATA)
                event_data = FirstEventData(data)
                browserEventsHandler.handle_event(event_data)
    except Exception as e:
        formatted_e = errors.EXCEPTION.format(
                fun=read_from_fifo.__name__,
                file=os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
                line=sys.exc_info()[2].tb_lineno,
                e=e,
            )
        print(formatted_e)
        logger.log(formatted_e)
        requestsHandler.getClient().close()
        raise e


def check_argv():
    """Using argparse library this function check arguments and set any variable required to be set"""
    global FIFO_PATH
    global browserEventsHandler
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="If set show a notification for every event detected even if they have 0 malicious entries", action="store_true")
    parser.add_argument("api-key", help="The API key from virus total website(account required)")
    parser.add_argument("--nt", help="The timeout, expressed in SECONDS, for notifications - DEFAULT is 5", default=5, type=int)
    args = parser.parse_args()
    if args.verbose:
        browserEventsHandler.__setattr__('verbose', True)

    try:
        browserEventsHandler.__getattribute__('notify_handler').set_timeout(args.nt)
    except Exception as e:
        print(errors.INVALID_ARGV.format(fun=check_argv.__name__, e=e))
        logger.log(errors.INVALID_ARGV.format(fun=check_argv.__name__, e=e))
        exit(-1)

    try:
        requestsHandler.setAPIKey(args.__getattribute__('api-key'))
    except Exception as e:
        print(errors.INVALID_ARGV.format(fun=requestsHandler.setAPIKey.__name__, e=e))
        logger.log(errors.INVALID_ARGV.format(fun=requestsHandler.setAPIKey.__name__, e=e))
        requestsHandler.getClient().close()
        exit(-1)


def signal_handler(sig, frame):
    """Handle signal like SIGTERM to shutdown properly"""
    os.write(sys.stdout.fileno(), b"\nTerminating...\n")
    logger.log("\nTerminating...\n")
    requestsHandler.getClient().close()
    sys.exit(0)


if __name__ == "__main__":
    main()
