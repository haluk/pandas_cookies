#!/usr/bin/env python3
import configparser


def read_config(config):
    """Reads config file

    Parameters
    ----------
    config : str
        config file path


    Returns
    -------
    out : configparser

    """

    cfg = configparser.ConfigParser()
    cfg.read(config)

    return cfg
