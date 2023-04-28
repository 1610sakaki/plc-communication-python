#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from logging import DEBUG, INFO, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


def set_log_config(logger, dir, filename):

    # ---- Prepare log folder ----
    os.makedirs(dir, exist_ok=True)
    filepath = dir + filename

    # ---- handler1: For terminal ----
    handler1 = StreamHandler()
    handler1.setLevel(DEBUG)
    handler1.setFormatter(
        Formatter("[%(asctime)s][%(levelname)8s][%(name)s][%(funcName)s] %(message)s")
    )

    # ---- handler2: For log file ----
    # handler2 = TimedRotatingFileHandler(filename = filepath, when='midnight', backupCount=30, encoding='utf-8') # If you want to rotate file by time, use this
    handler2 = RotatingFileHandler(
        filename=filepath,
        maxBytes=1048576,
        backupCount=10,
        encoding="utf-8",
    )  # 1MB, keep 10 files
    handler2.setLevel(INFO)
    handler2.setFormatter(
        Formatter("[%(asctime)s][%(levelname)8s][%(name)s][%(funcName)s] %(message)s")
    )

    # ---- Set log config ----
    logger.setLevel(DEBUG)
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    logger.propagate = False
