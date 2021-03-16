#!/usr/bin/env python3
#==============================================================================
#title           : testexample2_lib.py
#description     : Example test lib file to create classes or methods to
#                  control test execution.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Example test lib file to create classes or methods to control test execution.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from lib import log_lib as LOG
from lib import sys_lib as SYS
from lib import testctrl_lib as CTRL
from src.tests.testexample1.testconfig import testexample1_config as testCFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

#...

#==============================================================================
#============================ TEST DEFINITION =================================
#==============================================================================

test_def = {
    'type' : 'test',
    'name' : 'testexample2',
    'descp': 'Test to cover bla bla 2',
    'usermodes' : {
        'automation' : 1,
        'interactive' : 1,
        'gui' : 1
    },
    'test_cases' : {
        1 : { 'name' : 'firstmethod',  "descp" : "Method to test bla bla 1",
              'mode' : 'normal', 'concurrency_inst' : 1, 'protected' : 1},
        2 : { 'name' : 'secondmethod', "descp" : "Method to test bla bla 2",
              'mode' : 'concurrency', 'concurrency_inst' : 3, 'protected' : 1},
        3 : { 'name' : 'thirdmethod',  "descp" : "Method to test bla bla 3",
              'mode' : 'normal', 'concurrency_inst' : 1, 'protected' : 0}
        }
    }

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

#This class takes a base of Control class that contains methods
#to control test case execution to avoid mix control and test logic.
class testexample2(CTRL.TestController):
    """
    Class to extend functionality of testexample1 test.
    """

    def __init__(self):
        """
        Constructor
        """

        super().__init__(test_def)

    #==========================================================================

    def extraFunc(self, msg):
        """
        Example of functional extension

        type: str
        @param: msg - just a string message

        rtype: number
        @return: 0
        """

        self.log.logshow(testCFG.SW_2_MSG % msg, LOG.INFO)
        return 0
