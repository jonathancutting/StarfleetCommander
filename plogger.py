#!/usr/bin/env python3

import logging          # for built-in logging functionality
import sys              # for file I/O

class LoggingFallbackHandler(logging.FileHandler):
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