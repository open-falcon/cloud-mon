#!/usr/bin/python2
# -*- coding: utf-8 -*-
# by Laura 2018/05/31

import yaml
import logging.config
import os


def setup_logging(default_path="logging.yml",
                  default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            try:
                logging.config.dictConfig(config)
            except BaseException:
                os.makedirs('log/')
                logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def func():
    logging.info("start func")
    logging.info("exec func")
    logging.info("end func")
