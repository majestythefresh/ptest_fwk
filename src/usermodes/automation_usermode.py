#!/usr/bin/env python3
#==============================================================================
#title           : automation_usermode.py
#description     : Framework module to handle a config test_def dictionary
#                  for automation user mode.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Framework module to handle a config test_def dictionary
for automation user mode.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from config import config as CFG
from lib import sys_lib as SYS

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

#...

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

AUM_PROF_INCOMPLETE = 'Profile execution can\'t continue due missing test'

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class AutomationUserMode(object):
    """
    Class to extend functionality of user modes for Automation user mode.
    """
    def __init__(self):
        """
        Constructor
        """
        self.data = []

    #=========================================================================

    def getDefinition(self, type_def, name):
        """
        get test Defition according to user mode

        type: str
        @param: type_def - type of definition (profile | test)

        type: str
        @param: testname - name of definition

        rtype: dictionary
        @return: test definition
        """

        #Get configured definition
        testdef = LIB.getDefinition(type_def, name)
        if not testdef:
            SYS.exitTC(SYS.EXIT_ERROR)

        #Nesting test cases in case of profile
        if type_def == CFG.SW_TD_PROFILE:
            for profile_key, profile_value in testdef['tests'].items():
                test = LIB.getDefinition(CFG.SW_TD_TEST, profile_value['name'])
                if test:
                    testdef['tests'][profile_key]['usermodes']=test['usermodes']
                    testdef['tests'][profile_key]['test_cases']=test['test_cases']
                else:
                    print(AUM_PROF_INCOMPLETE)
                    SYS.exitTC(SYS.EXIT_ERROR)

        return testdef
