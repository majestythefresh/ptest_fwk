#!/usr/bin/env python3
#==============================================================================
#title           : testexample2_config.py
#description     : Example test config file to define HW and SW variables
#                  as constant.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Example test config file to define HW and SW variables as constant
"""

#==============================================================================
#=============================== CONFIG HW ====================================
#==============================================================================

HW_VTEST = 'HW constant from testexample2_config'

#==============================================================================
#=============================== CONFIG SW ====================================
#==============================================================================

SW_VTEST = 'SW constant from testexample2_config'

#Strings
SW_CMD_OUT_STR='CMD Out:\n %s'

#Messages
SW_1_MSG = '----> I will run for: %d secs'
SW_2_MSG = '----> PID: [ %d ]'
SW_3_MSG = 'Timeout!'
SW_4_MSG = 'Message from %s'
SW_5_MSG = 'Msg from extrafunctionality: %s'
