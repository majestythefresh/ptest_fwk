#!/usr/bin/env python3
#==============================================================================
#title           : testexample1.py
#description     : Example test file. It contains test cases as methods with
#                  description as comments and a data collection with method
#                  names, order of execution and mode.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Test to cover bla bla 1
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import sys_lib as SYS
from lib import log_lib as LOG
from lib import testctrl_lib as CTRL
from src.tests.testexample1.testlib import testexample1_lib as testLIB
from src.tests.testexample1.testconfig import testexample1_config as testCFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import time

#==============================================================================
#============================ TEST DEFINITION =================================
#==============================================================================

#Test definition structure
test_def = testLIB.test_def

#Test Lib Class
test = testLIB.testexample1()

#==============================================================================
#============================= TEST CASES =====================================
#==============================================================================

@CTRL.TestCase
def firstmethod(args):
    """
    Method to test bla bla 1
    """

    time.sleep(5)
    log.logshow('[ %s ] ' % args[1], LOG.SUCCESS, LOG.OK)
    return SYS.RC_NO_ERROR

#==============================================================================

@CTRL.TestCase
def secondmethod(args):
    """
    Method to test bla bla 2
    """

    test.extraFunc(testCFG.SW_1_MSG % args[1])
    time.sleep(10)
    log.logshow('[ %s ] ' % args[1], LOG.SUCCESS, LOG.OK)
    return SYS.RC_NO_ERROR

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

if __name__ == "__main__":
    log = LOG.Logging(sys.argv[5])
    test.main(sys.argv, globals(), log)
