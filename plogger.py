#!/usr/bin/env python3

import logging              # for built-in logging functionality
import sys                  # for standard I/O

LOG_FILE = "sfc.txt"        # default log file path
LOG_LEVEL = logging.DEBUG   # default log level

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
        :type record: logging.LogRecord
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

def config_root_logger(cfg:dict[str, str]) -> logging.Logger:
    '''
    Configures the root logger, based on configuration choices in parameter. If
    logging fails for whatever reason, a fallback handler is used, writing all
    further logs to the console.
    
    :param cfg: Plogger configs. If "output", "level", or "filePath" are missing
                or malformed, then defaults will be used.
    :type cfg: dict

    :return: Configured root logger. DO NOT USE. Always create module-level
             logger using logging.getLogger(__name__).
    :rtype: logging.Logger
    '''

    # Validate config parms.
    if (not "output" in cfg):
        print("No log output found in config. Defaulting to console.")
        cfg["output"] = "console"
    if (not "level" in cfg):
        print(f"No log level found in config. Defaulting to {logging.getLevelName(LOG_LEVEL)}.")
        cfg["level"] = logging.getLevelName(LOG_LEVEL)

    match cfg["level"].upper():
        case "CRITICAL": log_level = logging.CRITICAL
        case "ERROR": log_level = logging.ERROR
        case "WARNING": log_level = logging.WARNING
        case "INFO": log_level = logging.INFO
        case "DEBUG": log_level = logging.DEBUG
        case _:
            print(f"Invalid log level specified in config: {cfg['level']}. "
                  f"Defaulting to {logging.getLevelName(LOG_LEVEL)}.")
            log_level = LOG_LEVEL

    # Create the logging formatter.
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    # Get the root logger and apply handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Create the fallback (console) handler.
    # This handler will receive log messages if writing to the log file fails.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if (cfg["output"].lower() == "file"):
        # Create the primary file handler with fallback.
        f = LOG_FILE
        if ("filePath" in cfg): f = cfg["filePath"]
        file_handler = LoggingFileHandler(
            filename=f, fallback_handler=console_handler
        )
        file_handler.setFormatter(formatter)

        # NOTE: DO NOT add console handler! LoggingFileHandler takes care of this.
        root_logger.addHandler(file_handler)

        # Test that the log file can be written.
        try:
            with open(f, 'w') as fi:
                fi.write("")
                fi.close()
            root_logger.debug("Testing write to log file '%s'...", f)
        except OSError as e:
            root_logger.warning("Log file write failed! Subsequent log messages "
                                "will be printed to the console.")
    elif (cfg["output"].lower() == "console"):
        root_logger.addHandler(console_handler)

    root_logger.info("Logging level set to %s.", logging.getLevelName(root_logger.getEffectiveLevel()))
    return root_logger
