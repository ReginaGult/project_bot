# -*- coding: utf-8 -*-
"""
Created on Sat May 26 19:41:42 2018

@author: Vladimir
"""

# -*- coding: utf-8 -*-

from vedis import Vedis
import pictures_config as config


def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id]
        except KeyError: 
            return config.States.S_START.value 


def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False
