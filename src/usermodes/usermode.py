#!/usr/bin/env python3
#==============================================================================
#title           : usermode.py
#description     : Framework module to prepare a test_def dictionary
#                  based in user mode.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Framework module to prepare a test_def dictionary
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from config import config as CFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import importlib

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

UM_NOT_SUPPORT = 'ERROR: User Mode [ %s ] - Not supported yet'

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class UserMode(object):

    def __init__(self, usermode, args):
        """
        Constructor
        """
        self.usermode = usermode
        self.args = args

    def getDefinition(self, type_def, testname):
        """
        get test Defition according to user mode

        type: str
        @param: type_def - type of definition (profile | test)

        type: str
        @param: testname - name of definition

        rtype: dictionary
        @return: test definition
        """

        run_mode = ''
        test_id = ''
        log_folder = ''
        test_def = {}

        if self.usermode == CFG.SW_UM_AUTOMATION:
            amode = importlib.import_module('src.usermodes.automation_usermode')
            automation = amode.AutomationUserMode()
            run_mode = int(self.args[4])
            test_id=self.args[6]
            log_folder=self.args[5]
            test_def = automation.getDefinition(type_def, testname)

        elif self.usermode == CFG.SW_UM_INTERACTIVE:
            imode = importlib.import_module('src.usermodes.interactive_usermode')
            print (UM_NOT_SUPPORT % self.usermode)
            exit(1)
        elif self.usermode == CFG.SW_UM_GUI:
            user_gmode = importlib.import_module('src.usermodes.gui_usermode')
            gui = user_gmode.GuiUserMode(self.args)
            test_def, run_mode, test_id, log_folder = gui.getDefinition(type_def, testname)
        else:
            print (UM_NOT_SUPPORT % self.usermode)
            exit(1)

        return test_def, run_mode, test_id, log_folder
