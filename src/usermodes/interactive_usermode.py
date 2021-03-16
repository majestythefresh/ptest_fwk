#!/usr/bin/env python3
#==============================================================================
#title           : interactive_usermode.py
#description     : Framework module to handle a config test_def dictionary
#                  for interactive user mode.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Framework module to handle a config test_def dictionary
for interactive user mode.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from config import config as CFG


#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class IntercativeUserMode(object):

    def __init__(self):
        """
        Constructor
        """
        self.data = []
