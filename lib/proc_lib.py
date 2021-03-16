#!/usr/bin/env python3
#==============================================================================
#title           : common_lib.py
#description     : Library file to cover execution of subprocesses.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Library file to cover execution of subprocesses.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

#...

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import os
import signal
from subprocess import *

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#Strings
PROC_RUN = 'Running'
PROC_NOT_RUN = 'Not Running'
PROC_NO_PROC = 'No such process [ %d ]'
PROC_CMD_DCD_UTF8 = 'utf-8'

#Commands
PROC_CMD_INST_TC = 'ps aux | grep "%s.py %s" | grep -v $$ | grep -v -c "grep" ; sleep 1'
PROC_CMD_INST_TEST = 'ps aux | grep "%s.py" | grep -v $$ | grep -v -c "grep"'

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

def execProcDetch(command, proc_flag = False):
    """
    Execute a subprocess in detached mode

    @type: list
    @param: command - list with script and arguments

    @type: number
    @param: proc_flag - False (run command showing output) | True (run command
                             without showing output) (optional)

    @rtype: subprocess
    @return: process object
    """
    if proc_flag: #Hidde output
        process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    else: #Show output
        process = Popen(command)

    return process

#==============================================================================

def execProcWait(command, output_flag = False):
    """
    Execute a subprocess and wait to finish

    @type: list
    @param: command - list with script and arguments

    @type: number
    @param: output_flag - False (return an exit code only) | True (return exit code
                            and output in a var) (optional)

    @rtype: list of number and str
    @return: code and command output (optional)
    """
    if output_flag:
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        output, err = process.communicate()
        rc = process.returncode
        rout = output
        return rc, rout
    else:
        process = Popen(command)
        process.communicate()
        rc = process.returncode
        return rc

#==============================================================================

def listPids(procs, signal_prot):
    """
    list of detached subprocesses.

    @type: list of subprocess (Popen)
    @param: procs - list of subprocess objects

    @type: list
    @param: signal_prot - list of protected attributes against sys signals

    @rtype: list [pid, no. instance, 'Status', Exit code]
    @return: list of protected attribute
    """
    pids = []
    for i in range(len(procs)):
        pid = procs[i].pid
        pids.append([pid, (i+1), PROC_RUN, None, signal_prot[i]])

    return pids

#==============================================================================

def waitPids(procs, pids):
    """
    Put to wait a list of detached subprocesses and
    return array with status and exit code when
    all of them finished.

    @type: list (Popen)
    @param: procs - list of subprocess objects

    @type: list
    @param: pids - list of pids info

    @rtype: list [pid, no. instance, 'Status', "Exit: code"]
    @return: pid list with exit codes
    """
    for i in range(len(procs)):
        procs[i].wait()
        pids[i][2] = PROC_NOT_RUN
        pids[i][3] = procs[i].returncode
        pids[i][4] = 0

    return pids

#==============================================================================

def sendSignalPID(pid, signal):
    """
    send a sys signal to a process.

    @type: number
    @param: pid - process id

    @type: sys signal
    @param: signal - sys signal to send
    """
    try:
        os.kill(pid, signal)
    except:
        print(PROC_NO_PROC % pid)

#==============================================================================

def getInstances(testname, method = None):
    """
    Get instances running for a test and method

    @type: str
    @param: testname - test name

    @type: str
    @param: method - method name

    @rtype: number
    @return: number of instances running
    """
    proc_inst = 0
    if method:
        command = PROC_CMD_INST_TC % (testname, method)
    else:
        command = PROC_CMD_INST_TEST % (testname)
    result = run(command, shell=True, stdout=PIPE)
    proc_inst = int(result.stdout.decode(PROC_CMD_DCD_UTF8))
    #print ('Instances already running:', 0 if (proc_inst - 1) < 0 else (proc_inst - 1))
    return proc_inst
