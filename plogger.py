#!/usr/bin/env python3

import logging              # for built-in logging functionality
import sys                  # for standard I/O

LOG_FILE = "sfc.log"        # log file path. TODO: get this from config file
LOG_LEVEL = logging.DEBUG   # default logging level. TODO: get this from file

class LoggingFileHandler(logging.FileHandler):
    '''
    A file handler that falls back to a default logging handler (e.g., console),
    if an OSError occurrs while trying to write to the log file.
    '''

    def __init__(self, filename: str, mode: str = "a",
                 encoding: str | None = None, delay: bool = False,
                 errors: str | None = None,
                 fallback_handler:logging.Handler | None = None) -> None:
        super().__init__(filename, mode, encoding, delay, errors)
        # The handler to use if writing to the log file fails.
        self.fallback_handler = fallback_handler
        # Flag to signal that fallback has already occurred.
        self.is_fallback_active = False

    def emit(self, record:logging.LogRecord):
        '''
        Emits the log record. Tries to write to the log file. If an OSError
        occurs (e.g., permissions issue or disk full), it switches to the
        fallback handler and logs a CRITICAL message about the failure.
        
        :param record: LogRecord object containing the log record to emit.
        '''

        # If fallback is already active, use the fallback handler immediately.
        if self.is_fallback_active:
            if self.fallback_handler:
                self.fallback_handler.emit(record)
            return
        
        try:
            # Try to emit to the primary log handler.
            super().emit(record)
        except OSError as e:
            # An I/O error occurred (e.g. permissions, disk full, etc.).
            self.is_fallback_active = True # Activate fallback mode.

            # Create a CRITICAL log message about the failure.
            failure_message = (
                "CRITICAL: Failed to write to log file '%s'. "
                "ERROR: %s. Switching to console output.",
                self.baseFilename, e
            )

            # Log the failure message to the console.
            if self.fallback_handler:
                # Manually create the failure log record.
                failure_record = logging.makeLogRecord({
                    "name": record.name,
                    "level": logging.CRITICAL,
                    "pathname": __file__,
                    "lineno": sys._getframe().f_lineno,
                    "msg": failure_message,
                    "exc_info": None,
                    "func": "emit"
                })
                self.fallback_handler.emit(failure_record)

                # Now, emit the original message using the fallback handler.
                self.fallback_handler.emit(record)

def configRootLogger():
    '''
    Configures the root logger, then tests to see if log file can be opened and
    written. If it can't, logging will be defaulted to the console. Since this
    config is written to the root logger, and since this config is run before
    any external functions are used, all new logger objects will pull this
    config unless explicitly overwritten in that module.
    '''

    # Create the logging formatter.
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%s.%03d"
    )

    # Create the fallback (console) handler.
    # This handler will receive log messages if writing to the log file fails.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Create the primary file handler with fallback.
    file_handler = LoggingFileHandler(
        filename=LOG_FILE, fallback_handler=console_handler
    )
    file_handler.setFormatter(formatter)

    # Get the root logger and apply handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    # Add the fallback file handler.
    # NOTE: DO NOT add console handler! LoggingFileHandler takes care of this.
    root_logger.addHandler(file_handler)

    # Test that the log file can be written.
    try:
        with open(LOG_FILE, 'w') as f:
            f.write("")
        root_logger.debug("Attempting to write to log file '%s'...", LOG_FILE)
    except OSError as e:
        root_logger.warning("Log file write failed! Subsequent log messages "
                            "will be printed to the console.")

    return root_logger
