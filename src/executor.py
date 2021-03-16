#!/usr/bin/env python3
#==============================================================================
#title           : executor.py
#description     : Main framework module to execute test according to structure
#                  definition of a profile or test.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Main framework module to execute test according to structure
definition of a profile or test.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from config import config as CFG
from lib import sys_lib as SYS
from lib import proc_lib as PROCLIB
from lib import log_lib as LOG
from src.usermodes import usermode as uMode

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import os
import signal
import time
import datetime

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#Strings
EXC_PID_HEAD = '[[ %d ]] - Executor'
EXC_NO_UM_TEST = 'Test [%s] is not configured to run in current usermode [%s]'
EXC_RUN_PROC = '[ %d ] -> { %d } - To run process for: %s'
EXC_PROC_WAIT = '[ %d ] - Process List to wait: %s'
EXC_PROC_EXIT = '[ %d ] - Process(es) Exit Code(s): %s'
EXC_SIG_RCV = 'SIGNAL Received: %d'
EXC_PROC_INT = 'Interrupting processes running...'
EXC_PID_PROT = '! Protected PID %d - waiting to finish...'
EXC_PID_KILL = '* Killing PID: %s'
EXC_TEST_ERROR = 'Execution finished!: TEST ID [ %s ] ends with error(s)'
EXC_TEST_SUCESS = 'Execution finished!: TEST ID [ %s ] ends without error(s)'
EXC_TEST_ID_ERROR = 'Custom ID Test folder exist [ %s ] try another.'


#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class Executor(object):
    """
    Class to manage execution of profile or test
    """

    def __init__(self, usermode, log_path, log_custom_id=None):
        """
        Constructor
        """

        self.usermode = usermode
        self.procs = []
        self.exit_codes = []
        self.test_id = None
        if log_path:
            self.log_path = log_path
        else:
            self.log_path = CFG.SW_LOGS_PATH
        self.log_custom_id = log_custom_id

    #==========================================================================

    def setDefinition(self, test_def, procmode):
        """
        Set Defition function

        type: test definition dictionary
        @param: test_def - test definition

        type: number
        @param: procmode - run processes in Normal or Parallel (0 | 1)
        """

        self.procmode = procmode
        self.dft = test_def

        if self.dft:
            return SYS.RC_NO_ERROR
        else:
            return SYS.RC_ERROR

    #==========================================================================

    def start(self):
        """
        Start execution based on test/profile definition
        """

        #Setting up Test ID
        self.__setupTest()

        self.log.logshow(EXC_PID_HEAD % os.getpid(), LOG.DEBUG)
        self.log.writeJSON(LOG.JSON_START_DATE, [str(datetime.datetime.now())])
        self.log.writeJSON(LOG.JSON_MODE, [self.usermode])

        if self.dft['type'] == CFG.SW_TD_PROFILE:
            self.startProfile()
        else:
            self.log.writeJSON(LOG.JSON_TEST_EXEC)
            self.startTest()

        self.log.writeJSON(LOG.JSON_TEST_END)

        self.log.writeJSON(LOG.JSON_END_DATE, [str(datetime.datetime.now())])

        rc = self.__checkExitCode()
        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)
        if rc:
            self.log.logshow(EXC_TEST_ERROR % (self.test_id), LOG.FAILED, LOG.WRONG)
            self.log.writeJSON(LOG.JSON_EXIT_ST, [SYS.EXIT_ERROR])
            self.log.writeJSON(LOG.JSON_EXIT_MSG, [SYS.EXIT_ERROR_MSG])
        else:
            self.log.logshow(EXC_TEST_SUCESS % (self.test_id), LOG.PASSED, LOG.OK)
            self.log.writeJSON(LOG.JSON_EXIT_ST, [SYS.EXIT_NO_ERROR])
            self.log.writeJSON(LOG.JSON_EXIT_MSG, [SYS.EXIT_NO_ERROR_MSG])
        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)
        self.log.writeJSON(LOG.JSON_CHKSUM, [self.log.getTestIDSHA256(self.test_id)])

        if rc:
            return SYS.RC_ERROR

        return SYS.RC_NO_ERROR

    #==========================================================================

    def startTest(self):
        """
        Start execution based on test definition
        """

        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)
        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)
        self.log.logshow('{:^53}'.format('[ %s ]' % self.dft['name']), LOG.INFO)
        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)

        self.rcs = []
        signal_prots = []
        proc_obj = None

        #Check if test can run in usermode
        if not LIB.isTestAbleToRun(self.dft, self.usermode) :
            self.log.logshow(EXC_NO_UM_TEST % (self.dft['name'], self.usermode), LOG.WARNING, LOG.WRN)
            return

        self.log.writeJSON(LOG.JSON_TEST_NAME, [self.dft['name']] )

        #Run test cases sorted by order
        for k, v in sorted(self.dft['test_cases'].items()):

            cinst = int(v['concurrency_inst'])

            script = '%s/%s/%s.py' %(CFG.SW_TEST_PATH, self.dft['name'], self.dft['name'])
            argmt1 = v['name']
            argmt2 = v['mode']
            argmt4 = self.test_id
            argmt5 = self.log_path
            argmt6 = '%d' % k

            for conc_inst in range(cinst):
                argmt3 = '%s' % (conc_inst+1)
                cmd = [ script, argmt1, argmt2, argmt3, argmt4, argmt5, argmt6]
                proc_obj = PROCLIB.execProcDetch(cmd, False)
                self.log.logshow(EXC_RUN_PROC % (os.getpid(), proc_obj.pid, cmd), LOG.DEBUG)
                self.procs.append(proc_obj)
                signal_prots.append(v['protected'])
                time.sleep(1)

            #Wait for Sequential Mode
            if not self.procmode and self.procs:
                self.__waitExec(signal_prots)
                signal_prots = []

        #Wait for Parallel Mode
        if self.procmode and self.procs:
            self.__waitExec(signal_prots)

        return SYS.RC_NO_ERROR

    #==========================================================================

    def startProfile(self):
        """
        Start execution based ontype profile definition
        """

        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)
        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)
        self.log.logshow('{:^53}'.format('[ %s ]' % self.dft['name']), LOG.INFO)
        self.log.logshow(CFG.SW_SEP_STR, LOG.INFO)

        profile_def = self.dft

        self.log.writeJSON(LOG.JSON_PROFILE, [profile_def['name']])
        self.log.writeJSON(LOG.JSON_TEST_EXEC)

        for k, v in sorted(profile_def['tests'].items()):
            self.testdft = profile_def['tests'][k]
            self.setDefinition(self.testdft, self.procmode)
            rc = self.startTest()

        return SYS.RC_NO_ERROR

    #==========================================================================

    def stop(self, signum, frame):
        """
        Stop execution by signal trap

        type: signal
        @param: signum - sys signal

        type: stack
        @param: frame - stack traceback
        """

        flag_protected = 0

        self.log.logshow(EXC_SIG_RCV % signum, LOG.WARNING)
        self.log.logshow(EXC_PROC_INT, LOG.WARNING)
        self.log.logshow('%s' % self.rcs, LOG.WARNING)

        #Create exit file counter
        SYS.createExit(self.test_id)

        #In case of parallel mode write a lock file as flag
        if self.procmode:
            SYS.writeParallelMode(self.test_id)

        #Starting to check process properties list
        for proc in self.rcs:
            if proc[4]:#If test case protected flag is active
                self.log.logshow(EXC_PID_PROT % proc[0], LOG.WARNING)
                #Send SIGINT signal to process to exit in safety mode
                PROCLIB.sendSignalPID(proc[0], signal.SIGINT)
                #Parallel Mode
                if self.procmode: #Increment exit counter
                    SYS.writeValueExit(self.test_id)
                flag_protected |= 2
            else: #If test case is not protected kill it
                self.log.logshow(EXC_PID_KILL % proc[0], LOG.WARNING)
                PROCLIB.sendSignalPID(proc[0], signal.SIGKILL)
                time.sleep(1)
                flag_protected |= 1

        #If stop action performed in not protected only or no processes to exit
        if flag_protected == 1 or not self.rcs:
            #Remove exit counter
            SYS.removeExit(self.test_id)
            if self.procmode:#Remove parallel lock
                SYS.removeParallelMode(self.test_id)
            #Write Json report file footer
            try:
                self.log.writeJSON(LOG.JSON_END_DATE, [str(datetime.datetime.now())])
                self.log.writeJSON(LOG.JSON_EXIT_ST, [SYS.EXIT_BY_SIGNAL])
                self.log.writeJSON(LOG.JSON_EXIT_MSG, [SYS.getExitMsg(SYS.EXIT_BY_SIGNAL)])
                self.log.writeJSON(LOG.JSON_CHKSUM, [self.log.getTestIDSHA256(self.test_id)])
            except:
                pass

        SYS.exitTC(SYS.EXIT_BY_SIGNAL)

    #==========================================================================

    def __setupTest(self):
        """
        Set up Test with ID and output log path
        """

        if not self.test_id:
            self.log = LOG.Logging(self.log_path)
            if self.log_custom_id and self.log_custom_id != '':
                #check if custom name exist in path
                custom_id_folder = '%s/%s' % (self.log_path, self.log_custom_id)
                if os.path.exists(custom_id_folder):
                    print(EXC_TEST_ID_ERROR %  custom_id_folder)
                    SYS.exitTC(SYS.EXIT_ERROR)
                self.test_id = self.log_custom_id
            else:
                #Auto-Generate numeric ID
                self.test_id = self.log.getNewIDTest()

            #Set Log ID
            self.log.setTestLog(self.test_id)
            self.log.initJSON()

        return SYS.RC_NO_ERROR

    #==========================================================================

    def __checkExitCode(self, proc_list = None):
        """
        Check if there are exit code different from 0

        type: list
        @param: proc_list - process list with exit properties (optional)

        rtype: number
        @return: 0 success, 1 error
        """

        if proc_list: #check process list exit properties
            for i in range(len(proc_list)):
                if proc_list[i][3] != SYS.EXIT_NO_ERROR:
                    return SYS.RC_ERROR
        else: #Check just an exit codes list
            for i in range(len(self.exit_codes)):
                if self.exit_codes[i] != SYS.EXIT_NO_ERROR:
                    return SYS.RC_ERROR

        return SYS.RC_NO_ERROR

    #==========================================================================

    def __waitExec(self, signal_prots):
        """
        Wait for a list of processes to finish

        type: list
        @param: signal_prots - protected process list
        """

        #get process(es) init properties
        self.rcs = PROCLIB.listPids(self.procs, signal_prots)
        self.log.logshow(EXC_PROC_WAIT % (os.getpid(), self.rcs), LOG.DEBUG)
        #put to wait processes list
        self.rcs = PROCLIB.waitPids(self.procs, self.rcs)
        self.log.logshow(EXC_PROC_EXIT % (os.getpid(), self.rcs), LOG.DEBUG)
        #keep process(es) exit code(s) for final status
        self.exit_codes.append(self.__checkExitCode(self.rcs))
        self.procs = []



#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """
    #Check if custom definition is received
    if args[1] == CFG.SW_CUSTOM_TD:
        if args[2]:
            test_def = args[2]
            user_mode = CFG.SW_UM_AUTOMATION
            proc_mode = int(args[3])
            try:
                log_path=args[4]
                log_custom_id=args[5]
            except:
                log_path = None
                log_custom_id = None
    else: #If not, do normal execution of user modes
        if len(args) < 5 :
            CFG.SW_EXECUTOR_USAGE()
            SYS.exitTC(SYS.EXIT_ERROR)

        type_def = args[1]
        name = args[2]
        user_mode = args[3]
        proc_mode = int(args[4])
        try:
            log_path=args[5]
            log_custom_id=args[6]
        except:
            log_path = None
            log_custom_id = None

        #TODO: User Modes (gui, interactive, web)
        #Get definiton from UserMode Class based in user mode selected
        usermode = uMode.UserMode(user_mode, args)
        test_def, proc_mode, log_custom_id, log_path = usermode.getDefinition(type_def, name)

    if not test_def:
        SYS.exitTC(SYS.EXIT_ERROR)

    exect = Executor(user_mode, log_path, log_custom_id)
    # set signal traps
    signal.signal(signal.SIGINT, exect.stop)
    signal.signal(signal.SIGTERM, exect.stop)
    #Set definition
    rc = exect.setDefinition(test_def, proc_mode)
    if not rc:
        # Exec test definition
        rc = exect.start()

    SYS.exitTC(rc)


if __name__ == "__main__":
    main(sys.argv)
