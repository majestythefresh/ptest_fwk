#!/usr/bin/env python3
#==============================================================================
#title           : testexample2.py
#description     : Example test file. It contains test cases as methods with
#                  description as comments and a data collection with method
#                  names, order of execution and mode.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Test to cover bla bla 2
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import sys_lib as SYS
from lib import log_lib as LOG
from lib import testctrl_lib as CTRL
from src.tests.testexample2.testlib import testexample2_lib as testLIB
from src.tests.testexample2.testconfig import testexample2_config as testCFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import time
import os
from random import randint

#==============================================================================
#============================= TEST DEFINITION ================================
#==============================================================================

#Test definition structure
test_def = testLIB.test_def

#Test Lib Class
test = testLIB.testexample2()

#==============================================================================
#============================= TEST CASES =====================================
#==============================================================================

@CTRL.TestCase
def firstmethod(args):
    """
    Method to test bla bla 1
    """

    time.sleep(5)
    rc, rout = SYS.execCommand(['ls','-l'], 2, 1)
    if rc == SYS.EXIT_TIMEOUT:
        log.logshow(testCFG.SW_3_MSG, LOG.WARNING, LOG.WRN)
        log.logshow('[ %s ] ' % args[1], LOG.ERROR, LOG.WRONG)
    else:
        log.logshow(testCFG.SW_CMD_OUT_STR % rout, LOG.INFO)
        log.logshow('[ %s ] ' % args[1], LOG.SUCCESS, LOG.OK)
    time.sleep(5)
    return SYS.RC_NO_ERROR

#==============================================================================

@CTRL.TestCase
def secondmethod(args):
    """
    Method to test bla bla 2
    """

    rnum = randint(0, 20)
    log.logshow(testCFG.SW_1_MSG % rnum, LOG.DEBUG)
    time.sleep(rnum)
    log.logshow(testCFG.SW_2_MSG % os.getpid(), LOG.DEBUG)
    if rnum == SYS.RC_NO_ERROR:
        log.logshow('[ %s ] [ %s ]'% ( args[1], args[3]), LOG.SUCCESS, LOG.OK)
    else:
        log.logshow('[ %s ] [ %s ]' % ( args[1], args[3]), LOG.ERROR, LOG.WRONG)
    return rnum

#==============================================================================

@CTRL.TestCase
def thirdmethod(args):
    """
    Method to test bla bla 3
    """

    test.extraFunc(testCFG.SW_4_MSG % args[1])
    time.sleep(5)
    log.logshow('[ %s ] ' % args[1], LOG.ERROR, LOG.WRONG)
    return SYS.RC_ERROR

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

if __name__ == "__main__":
    log = LOG.Logging(sys.argv[5])
    test.main(sys.argv, globals(), log)
