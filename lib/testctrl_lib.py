#!/usr/bin/env python3
#==============================================================================
#title           : testctrl_lib.py
#description     : Test Controller library to control access for execution
#                  or stop events.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Test Controller library to control access for execution or stop events
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from lib import sys_lib as SYS
from lib import proc_lib as PROCLIB
from lib import log_lib as LOG
from config import config as CFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import importlib
import datetime
import os
import signal

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#Strings
CTRL_MOD_PROFILE = 'profiles.%s'
CTRL_MOD_TEST = 'tests.%s.%s'
CTRL_TD_NOTVALID = 'Definition type is not valid'
CTRL_TEST_ID = 'TEST ID [ %s ]'
CTRL_ENTER_TEST = 'Entering Test [ %s ]'
CTRL_TESTCASE = 'Test Case [ %s ]'
CTRL_TESTCASE_ORDER = 'Order [ %d ]'
CTRL_TESTCASE_ARGS  = 'Parameters [ %s ]'
CTRL_TC_MODE = 'Mode [ %s ]'
CTRL_TC_DESCP = 'Description [ %s ]'
CTRL_TC_INST = 'Instance No. [ %s ]'
CTRL_EXIT_TEST = 'Exited Test [ %s ]'
CTRL_RC = 'Return Code [ %d ]'
CTRL_ERROR_MODE = 'ERROR: Mode [ %s ] - Invalid '
CTRL_SUPPORT_MODE = 'Supported [ %s ]'
CTRL_INST_NOTVALID = 'Test case [ %s ] -> [ %s ] in concurrency mode can not run more than (%d) times.'
CTRL_EXIT_PROC = 'Exit Counter: [ %d ] - Processes Alive: [ %d ]'

#Strings
CTRL_START_TC_STR = 'Starting testcase...'
CTRL_SIGNAL_RCV_STR = 'SIGNAL Received: %d in test: [ %s ] - test case [ %s ] - instance [ %s ]'
CTRL_TC_PROT_STR = 'Test case protected - Waiting to finish...'
CTRL_INT_TEST_STR = 'Interrupting Test(s) running...'


#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

#This class is a decorator class that contains methods
#to execute logic & control before and after test case run.
class TestCase(object):
    """
    Decorator Class to protect function to run with incorrect mode and more than
    configured instances.
    """

    def __init__(self, test_case):
        """
        Constructor.
        """
        self.test_case = test_case

    #==========================================================================

    def __call__(self, args, tdef, test_ctrl, log):
        """
        Function to work as rules keeper after and before execution.

        type: sys.argv
        @param: args - argument list (method, mode, instance number)

        type: test_def
        @param: test_def - test definition structure

        type: Logging
        @param: log - log object

        """

        method = args[1]
        mode = args[2]
        num_instance = args[3]
        test_id = args[4]
        order = args[6]

        #Getting attributes from test case
        attr = LIB.getMethodAttr(method, order, tdef)
        config_order = attr['order']
        config_test_name = attr['testname']
        config_name = attr['methodname']
        config_descp = attr['descp']
        config_mode = attr['mode']
        config_cinst = attr['cinst']
        config_args = attr['user_args']

        #Writing Test case header to log
        log_path = log.getLogPath()
        exec_log = LOG.Logging(log_path)
        exec_log.setTestLog(test_id)
        exec_log.log(CFG.SW_SEP_STR, LOG.INFO)
        exec_log.log(CTRL_TEST_ID % test_id, LOG.INFO)
        exec_log.log(CTRL_ENTER_TEST % config_test_name, LOG.INFO)
        exec_log.log(CTRL_TESTCASE % self.test_case.__name__ , LOG.INFO)
        exec_log.log(CTRL_TESTCASE_ORDER % config_order, LOG.INFO)
        exec_log.log(CTRL_TESTCASE_ARGS % config_args, LOG.INFO)
        exec_log.log(CTRL_TC_MODE % config_mode, LOG.INFO)
        exec_log.log(CTRL_TC_DESCP % config_descp, LOG.INFO)
        exec_log.log(CTRL_TC_INST % num_instance, LOG.INFO)
        log.logshow(CFG.SW_SEP_STR, LOG.INFO)
        log.logshow(CTRL_TEST_ID % test_id, LOG.INFO)
        log.logshow(CTRL_ENTER_TEST % config_test_name, LOG.INFO)
        log.logshow(CTRL_TESTCASE % self.test_case.__name__ , LOG.INFO)
        log.logshow(CTRL_TESTCASE_ORDER % config_order, LOG.INFO)
        log.logshow(CTRL_TESTCASE_ARGS % config_args, LOG.INFO)
        log.logshow(CTRL_TC_MODE % config_mode, LOG.INFO)
        log.logshow(CTRL_TC_DESCP % config_descp, LOG.INFO)
        log.logshow(CTRL_TC_INST % num_instance, LOG.INFO)

        #Protecting to override mode in functions than configured
        if config_mode != mode:
            log.show(CTRL_ERROR_MODE % mode, LOG.ERROR, LOG.WRONG)
            log.show(CTRL_SUPPORT_MODE % config_mode, LOG.INFO)
            SYS.exitTC(SYS.EXIT_ERROR)
        if mode == CFG.SW_TC_CONC or mode == CFG.SW_TC_NORMAL:
            #Protecting to run more instances than configured
            rout = PROCLIB.getInstances(config_test_name, self.test_case.__name__)
            if rout > int(config_cinst):
                log.logshow(CTRL_INST_NOTVALID % (config_test_name, self.test_case.__name__, config_cinst), LOG.ERROR, LOG.WRONG)
                exit (SYS.EXIT_ERROR)
        else:
            log.show(CTRL_ERROR_MODE % mode, LOG.ERROR, LOG.WRONG)
            SYS.exitTC(SYS.EXIT_ERROR)

        #Init test case properties
        test_ctrl.initTestCase(args, log)
        #Get start time
        start_time = datetime.datetime.now()
        #add user arguments to framework arguments
        if config_args:
            user_args = config_args.split(',')
            args.append(user_args)
        #calling test case
        rc = self.test_case(args)
        #Get end time
        end_time = datetime.datetime.now()

        #Write to log at end of each test case
        exec_log.log(CTRL_EXIT_TEST % config_test_name, LOG.INFO)
        exec_log.log(CTRL_TESTCASE % self.test_case.__name__ , LOG.INFO)
        exec_log.log(CTRL_TESTCASE_ARGS % config_args, LOG.INFO)
        exec_log.log(CTRL_TC_INST % num_instance, LOG.INFO)
        exec_log.log(CTRL_RC % rc, LOG.INFO)
        exec_log.log(CFG.SW_SEP_STR, LOG.INFO)
        log.logshow(CTRL_EXIT_TEST % config_test_name, LOG.INFO)
        log.logshow(CTRL_TESTCASE % self.test_case.__name__ , LOG.INFO)
        log.logshow(CTRL_TESTCASE_ARGS % config_args, LOG.INFO)
        log.logshow(CTRL_TC_INST % num_instance, LOG.INFO)
        log.logshow(CTRL_RC % rc, LOG.INFO)
        log.logshow(CFG.SW_SEP_STR, LOG.INFO)

        #Write JSON execution info
        log.writeJSON(LOG.JSON_TESTC, [config_test_name ,self.test_case.__name__ ,str(start_time), str(end_time), config_mode,num_instance,rc,SYS.getExitMsg(rc), config_args, config_order])

        #In case that sys signal was emitted, all processes (test cases) running with protected Mode
        # need to finish to write JSON footer info
        flag_write_footer_json = False
        #Check if signal set protected flag inside test case
        if test_ctrl.getProtSignalEmit():
            #End Json in case of protected test by kill signal
            if SYS.isParallelMode(test_id): #Process in Parallel mode
                #Per exited test case substract 1
                SYS.writeValueExit(test_id, True)
                exit_conc = SYS.readValueExit(test_id)
                #check if list was processed or there are 1(-1 = 0) instances of test
                log.show(CTRL_EXIT_PROC % (int(exit_conc), PROCLIB.getInstances(config_test_name) - 1), LOG.DEBUG)
                if int(exit_conc) <= 0 or (PROCLIB.getInstances(config_test_name) - 1) <= 0:
                    SYS.removeExit(test_id)
                    SYS.removeParallelMode(test_id)
                    flag_write_footer_json = True
            else: #Process in Sequential mode
                #Per exited test case add 1
                SYS.writeValueExit(test_id)
                exit_conc = SYS.readValueExit(test_id)
                log.show(CTRL_EXIT_PROC % (int(exit_conc), PROCLIB.getInstances(config_test_name) - 1), LOG.DEBUG)
                if int(exit_conc) >= int(config_cinst) or (PROCLIB.getInstances(config_test_name) - 1) <= 0:
                    SYS.removeExit(test_id)
                    flag_write_footer_json = True
            #Ready to write JSON footer
            if flag_write_footer_json:
                log.writeJSON(LOG.JSON_END_DATE, [str(datetime.datetime.now())])
                log.writeJSON(LOG.JSON_EXIT_ST, [SYS.EXIT_BY_SIGNAL])
                log.writeJSON(LOG.JSON_EXIT_MSG, [SYS.getExitMsg(SYS.EXIT_BY_SIGNAL)])
                log.writeJSON(LOG.JSON_CHKSUM, [log.getTestIDSHA256(test_id)])

        #Exit with function Return code : RC Output
        SYS.exitTC(rc)


#==============================================================================

#This class is a base of Control class that contains methods
#to control test case execution to avoid mix control and test logic.
class TestController(object):
    """
    Control Class for test.
    """

    def __init__(self, test_def):
        """
        Constructor
        """

        self.test_def = test_def
        self.testrunning = None
        self.no_instance = None
        self.log = None
        self.prot_signal_emit = False
        signal.signal(signal.SIGINT, self.stopTestBySignal)
        signal.signal(signal.SIGTERM, self.stopTestBySignal)

#==========================================================================

    def main(self, args, globals_def, log):
        """
        Main function for test.

        type: list
        @param: args - arguments that called test case

        type: globals[]
        @param: globals list of methods in package

        """

        attr = LIB.getMethodAttr(args[1], args[6], self.test_def)
        #Set Logging
        log.setTestLog(args[4], attr['testname'], args[1], args[3])
        #Test Main function
        LIB.main(args, self.test_def, self, log, globals_def)

    #==========================================================================

    def initTestCase(self, args, log):
        """
        Init Test Case passing arguments and log object.

        type: list
        @param: args - arguments that called test case

        type: Logging object
        @param: log - logging object to handle inside of extended class
        """

        self.testrunning = args[1]
        self.no_inst = args[3]
        self.order = args[6]
        if(len(args) > 7):
            self.args = args[7]
        else:
            self.args = ''
        self.log = log
        self.start_time = datetime.datetime.now()
        log.logshow(CTRL_START_TC_STR, LOG.INFO)

    #==========================================================================

    def stopTestBySignal(self, signum, frame):
        """
        Stop execution in test case by signal trap

        type: signal
        @param: signum - sys signal

        type: stack
        @param: frame - stack traceback
        """

        #If test case initialized
        if self.testrunning:
            tdef = LIB.getMethodAttr(self.testrunning, self.order, self.test_def)
            self.log.logshow(CTRL_SIGNAL_RCV_STR % ( signum, tdef['testname'], self.testrunning, self.no_inst ), LOG.WARNING)
            if tdef['protected'] == 1 :
                self.log.logshow(CTRL_TC_PROT_STR, LOG.WARNING)
                #Signal emit flag for protected test case
                self.prot_signal_emit = True
                #Return to wait to finish
                return

        #Finish the test case execution with an exit by signal code
        end_time = datetime.datetime.now()
        if self.log:
            self.log.logshow(CTRL_INT_TEST_STR, LOG.WARNING)
            self.log.writeJSON(LOG.JSON_TESTC, [ tdef['testname'], self.testrunning, str(self.start_time), str(end_time), tdef['mode'], str(self.no_inst), str(SYS.EXIT_BY_SIGNAL), SYS.getExitMsg(SYS.EXIT_BY_SIGNAL), self.args,  self.order ] )

        SYS.exitTC(SYS.EXIT_BY_SIGNAL)

    #==========================================================================

    def getTestCaseArgs(self, args):
        """
        Get dictionary of  test case arguments come from test definition

        type: list
        @param: args - framework argument list

        rtype: collection
        @return: dictionary with arguments
        """

        argmts = {}

        if(len(args) > 7):
            for arg in args[7]:
                key, value = arg.split('=')
                argmts[key] = value

            return argmts

        return {}

    #==========================================================================

    def getProtSignalEmit(self):
        """
        Get signal emit flag

        rtype: boolean
        @return: flag
        """

        return self.prot_signal_emit
