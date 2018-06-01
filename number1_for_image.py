# -*- coding: utf-8 -*-
"""
Created on Sat May 26 17:33:27 2018

@author: Vladimir
"""


# -*- coding: utf-8 -*-

import telebot


from enum import Enum

token = '607054617:AAGQqyok0jvt1lKvpSqCjvTP7_f6C21RENA'
db_file = "pictures.vdb"



class States(Enum):
    S_START = "0" 
    S_ENTER_NAME = "1"
    S_SEND_PIC = "2"