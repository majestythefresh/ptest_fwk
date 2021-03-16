#!/usr/bin/env python3
#==============================================================================
#title           : sys_lib.py
#description     : Library to cover the system task functions.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Library to cover the system task functions.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from config import config as CFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import os
from subprocess import *
import time
from pathlib import Path

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#Exit codes
EXIT_TIMEOUT = -1
EXIT_NO_ERROR = 0
EXIT_ERROR = 1
EXIT_BY_SIGNAL = 2

#Return codes
RC_NO_ERROR = 0
RC_ERROR = 1

#Exit Messages
EXIT_TIMEOUT_MSG = 'Timeout exit (%d)' % EXIT_TIMEOUT
EXIT_NO_ERROR_MSG = 'Exit without error (%d)' % EXIT_NO_ERROR
EXIT_ERROR_MSG = 'Exit with error (%d)' % EXIT_ERROR
EXIT_BY_SIGNAL_MSG = 'System signal (%d), exit.' % EXIT_BY_SIGNAL
EXIT_UNKNOW_MSG = 'Unknow reason exit'

#Strings
SYS_CMD_DCD_ASCII = 'ascii'
SYS_CMD_DCD_UTF8 = 'utf-8'
SYS_CMD_TIMEOUT = 'command timeout'
SYS_CONC_INIT_VAL = '0'
SYS_LCK_WAIT = 'Waiting lock to released'
SYS_NO_LCK_File = 'No Lock file'

#Files
SYS_CONC_CNT_FILE = 'exit_conc'
SYS_CONC_LCK_FILE = 'exit_conc.lock'
SYS_CONC_PARLCK_FILE = 'exit_conc_par.lock'

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

def execPlainCommand(command):
    """
    Execute a command with plain str command

    @type: str
    @param: command - command string

    @rtype: list of number and str
    @return: code and command output (optional)
    """

    process = Popen(args=command, stdout=PIPE, shell=True)

    try:
        return process.communicate()[0].decode(SYS_CMD_DCD_UTF8).split()[0]
    except:
        return ''

#==============================================================================

def execCommand(command, timeout = None, output_flag = 0):
    """
    Execute a command with a timeout (optional) and return data (optional)

    @type: list
    @param: command - list with script and arguments

    @type: number
    @param: timeout - seconds to wait before raise a timeout

    @type: number
    @param: output_flag - 0 (return an exit code only) | 1 (return exit code
                            and output in a var) (optional)
                            | 2 (realtime output, no timeout available)

    @rtype: list of number and str
    @return: code and command output (optional)
    """

    if output_flag == 1:
        try:
            result = run(command, timeout=timeout, stdout=PIPE, stderr=PIPE)
            if result.returncode:
                return result.returncode, result.stderr.decode(SYS_CMD_DCD_ASCII)
            else:
                return result.returncode, result.stdout.decode(SYS_CMD_DCD_ASCII)
        except TimeoutExpired:
            return EXIT_TIMEOUT, SYS_CMD_TIMEOUT
        except FileNotFoundError as e:
            return EXIT_ERROR, e
    if output_flag == 2:
        rout = ''
        try:
            result = Popen(command, stdout=PIPE, stderr=PIPE)
            while True:
                line = result.stdout.readline().decode(SYS_CMD_DCD_ASCII)
                print(line)
                rout = '%s\n%s' % (rout, line)
                if not line: break

            return result.returncode, rout

        except FileNotFoundError as e:
            return EXIT_ERROR, e
    else:
        try:
            result = run(command, timeout=timeout)
            return result.returncode
        except TimeoutExpired:
            return EXIT_TIMEOUT

#==============================================================================

def runShellCommand (command, timeout=None) :
    """
    run a command equal than shell with timeout (optional)

    @type: string
    @param: command - string with command

    @type: number
    @param: timeout - seconds to wait before raise a timeout

    @rtype: list of number and str
    @return: code and command output
    """
    try:
        result = run(command, timeout=timeout, shell=True, stdout=PIPE)
    except TimeoutExpired:
        return EXIT_TIMEOUT, SYS_CMD_TIMEOUT

    return result.returncode, result.stdout.decode(SYS_CMD_DCD_UTF8)

#==============================================================================

def exitTC(exit_code):
    """
    Exit with a code number.

    type: number
    @param: exit_code - code of exit

    """

    exit (exit_code)

#==============================================================================

def getExitMsg(exit_code):
    """
    Get a message from code number.

    type: number
    @param: exit_code - code of exit

    rtype: string
    @return: exit msg
    """

    if exit_code == EXIT_TIMEOUT:
        return EXIT_TIMEOUT_MSG
    elif exit_code == EXIT_NO_ERROR:
        return EXIT_NO_ERROR_MSG
    elif exit_code == EXIT_ERROR:
        return EXIT_ERROR_MSG
    elif exit_code == EXIT_BY_SIGNAL:
        return EXIT_BY_SIGNAL_MSG
    else:
        return EXIT_UNKNOW_MSG

#==============================================================================
#================ FUNCTIONS to keep integrity in JSON Output ==================
#==============================================================================

def createExit(test_id):
    """
    create exit file to keep concurrent processes (test cases) exit state.

    """

    exit_file = open('%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_CNT_FILE),'w')
    exit_file.write(SYS_CONC_INIT_VAL)
    exit_file.close()

#==============================================================================

def readValueExit(test_id):
    """
    Read instance counter value for concurrent processes (test cases) exit.

    type: string
    @param: test_id - Test ID string

    rtype: str
    @return: string as value, 0 if error to open file
    """

    try:
        exit_file = open('%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_CNT_FILE),'r')
        line = exit_file.readline()
        exit_file.close()
        return line
    except:
        return 0

#==============================================================================

def writeValueExit(test_id, op = False):
    """
    Write counter value for concurrent processes (test cases) exit.

    type: string
    @param: test_id - Test ID string

    type: boolean
    @param: op - add or substract to value from file (flag True = -1, False = +1)
    """

    lock_pathfile = '%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_LCK_FILE)
    exit_pathfile = '%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_CNT_FILE)
    while (isLock(lock_pathfile)):
        print(SYS_LCK_WAIT)
        time.sleep(1)

    #create lock
    lock_file = open(lock_pathfile,'w')
    lock_file.close()
    #Read value and add/substract 1 per test case finished
    if op:
        val = int(readValueExit(test_id)) - 1
    else:
        val = int(readValueExit(test_id)) + 1
    exit_file = open(exit_pathfile,'w')
    exit_file.write('%d' % val)
    exit_file.close()
    try:
        os.remove(lock_pathfile)
    except:
        print(SYS_NO_LCK_File)

#==============================================================================

def writeParallelMode(test_id):
    """
    Set lock file to indicate processes (test cases) were run in parallel mode.

    type: string
    @param: test_id - Test ID string
    """

    lock_pathfile = '%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_PARLCK_FILE)

    #create lock
    lock_file = open(lock_pathfile,'w')
    lock_file.close()

#==============================================================================

def isParallelMode(test_id):
    """
    Get boolean if test cases were run in parallel mode.

    type: string
    @param: test_id - Test ID string

    rtype: boolean
    @return: True if lock file exists, false otherwise
    """

    lock_pathfile = '%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_PARLCK_FILE)
    return isLock(lock_pathfile)

#==============================================================================

def isLock(file):
    """
    Get boolean if lock file exists.

    type: string
    @param: test_id - Test ID string

    rtype: boolean
    @return: True if lock file exists, false otherwise
    """

    return Path(file).exists()

#==============================================================================

def removeExit(test_id):
    """
    Remove concurrency counter file.

    type: string
    @param: test_id - Test ID string
    """

    os.remove('%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_CNT_FILE))

#==============================================================================

def removeParallelMode(test_id):
    """
    Remove parrallel lock file.

    type: string
    @param: test_id - Test ID string
    """

    os.remove('%s/%s/%s' % (CFG.SW_LOGS_PATH,test_id, SYS_CONC_PARLCK_FILE))
