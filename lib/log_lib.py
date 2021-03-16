#!/usr/bin/env python3
#==============================================================================
#title           : log_lib.py
#description     : Library to cover logging functions.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Library to cover logging functions.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from lib import sys_lib as SYS
from config import config as CFG


#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import datetime
import os
import re
from subprocess import *
from pathlib import Path
import json

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#Logging tags
INFO = "INFO"
ERROR = "ERROR"
WARNING = "WARNING"
DEBUG = "DEBUG"
SUCCESS = "SUCCESS"

#status labels
OK = "OK"
WRONG = "X"
PASSED = "PASSED"
FAILED = "FAILED"
WRN = "WRN"

#Commands
CMD_SHA256_TESTID_DIR = 'find %s/%s -type f ! -name "%s.json" -exec shasum -a 256 {} \; | shasum -a 256'

#Json ids
JSON_INIT = 'init'
JSON_END = 'end'
JSON_TEST_END = 'test_end'
JSON_END_ARRAY = 'end_array'
JSON_START_DATE = 'start_date'
JSON_END_DATE = 'end_date'
JSON_PROFILE = 'profile'
JSON_MODE = 'mode'
JSON_SHA256 = 'sha256sum'
JSON_TEST_EXEC = 'test_execution'
JSON_TEST_NAME = 'test_name'
JSON_TESTC = 'testc_exec'
JSON_EXIT_ST = 'exit_status'
JSON_EXIT_MSG = 'exit_msg'
JSON_CHKSUM = 'checksum'

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================= CLASSES ====================================
#==============================================================================

class Logging(object):
    """
    Class for logging
    """

    def __init__(self, log_path):
        """
        Constructor
        """

        self.log_path = log_path

    #==========================================================================

    def getNewIDTest(self):
        """
        Get New ID Test to start a set of tests.

        rtype: str
        @return: Test ID string
        """

        folders = []
        for folder in os.listdir(self.log_path):
            if re.search('[0-9]{6}', folder):
                folders.append(folder)
        if folders:
            ids = sorted(folders, reverse=True)
            id_test = '%06d' % (int(ids[0]) + 1)
            return id_test
        else:
            return CFG.SW_TEST_ID_INIT

    #==========================================================================

    def getIDTest(self):
        """
        Get Instance ID Test.

        rtype: str
        @return: Test ID string
        """

        return self.test_id

    #==========================================================================

    def getTestIDSHA256(self, test_id):
        """
        Get test id folder SHA 256 sum.

        rtype: str
        @return: Test ID string
        """
        rout = SYS.execPlainCommand(CMD_SHA256_TESTID_DIR % ( self.log_path, test_id, test_id))

        return rout.split()[0]

    #==========================================================================

    def getLogPath(self):
        """
        Get Instance Log Path.

        rtype: str
        @return: Log Path string
        """

        return self.log_path

    #==========================================================================

    def getJsonPath(self):
        """
        Get Instance Json Path.

        rtype: str
        @return: Log Path string
        """

        return self.test_json

    #==========================================================================

    def setTestLog(self, test_id, test_name = None, testc_name = None, test_inst = None):
        """
        Create folder and log files in a defined path.

        type: string
        @param: test_id - Test ID string (optional)

        type: string
        @param: test_name - Test name string (optional)

        type: string
        @param: testc_name - Test case name string (optional)

        type: string
        @param: test_inst- Test Instance number (optional)

        rtype: number
        @return: rc - return code

        """
        self.test_id = test_id

        #Create folder
        test_log_path = '%s/%s' % (self.log_path, test_id)
        rc, rout = SYS.execCommand(['mkdir','-p',test_log_path], None, 1)
        if not rc:
            self.test_json = '%s/%s.json' % ( test_log_path, test_id )
            rc, rout = SYS.execCommand(['touch',self.test_json], None, 1)

        #Create log file
        if not rc:
            if test_name: #Log file for test cases
                self.test_log_file = '%s/%s_%s_%s.log' % ( test_log_path,  test_name,
                                                      testc_name, test_inst)
            else: #Log file Different from test, like general log (optional parameters don't apply)
                self.test_log_file = '%s/%s.log' % ( test_log_path, test_id )
            rc, rout = SYS.execCommand(['touch', self.test_log_file], None, 1)

        return rc

    #==========================================================================

    def log(self, msg, tag = None, status = None):
        """
        Write msg in log file.

        type: str
        @param: msg - Message string

        type: str
        @param: tag - tag string

        type: str
        @param: status - status string

        """
        if not tag:
            tag = INFO

        if not CFG.SW_LOG_DEBUG and tag == DEBUG:
            return

        date_time = datetime.datetime.now()

        if status:
            log_line = '[ %s ] [ %s ] %s [ %s ]\n' % (date_time, tag, msg, status)
        else:
            log_line = '[ %s ] [ %s ] %s\n' % (date_time, tag, msg)

        log_file = open(self.test_log_file,'a')
        log_file.write(log_line)
        log_file.close()

    #==========================================================================

    def show(self, msg, tag = None, status = None):
        """
        Write msg in log file.

        type: str
        @param: msg - Message string

        type: str
        @param: tag - tag string

        type: str
        @param: status - status string

        """
        if not tag:
            tag = INFO

        if not CFG.SW_LOG_DEBUG and tag == DEBUG:
            return

        date_time = datetime.datetime.now()

        if status:
            if status == OK or status == PASSED :
                status ='\x1b[1;32m'+ status + '\x1b[0m'
            if status == WRONG or status == FAILED :
                status ='\x1b[1;31m'+ status + '\x1b[0m'
            if status == WRN :
                status ='\x1b[1;33m'+ status + '\x1b[0m'
            log_line = '[ %s ] [ %s ] - %s [ %s ]' % (date_time, tag, msg, status)
        else:
            log_line = '[ %s ] [ %s ] - %s' % (date_time, tag, msg)

        print(log_line)

    #==========================================================================

    def logshow(self, msg, tag = None, status = None):
        """
        Write msg in log file.

        type: str
        @param: msg - Message string

        type: str
        @param: tag - tag string

        type: str
        @param: status - status string

        """
        self.show(msg, tag, status)
        self.log(msg, tag, status)

    #==========================================================================

    def writeJSON(self, element, value = None):
        """
        Write msg in log file.

        type: str
        @param: element - element name

        type: list
        @param: value - list with nested values for element
        """

        lock_pathfile = '%s/%s/%s.json.lock' % (self.log_path, self.test_id, self.test_id)
        while(not Path(lock_pathfile).exists()):
            lock_file = open(lock_pathfile,'w')
            lock_file.close()

            json_file = open(self.test_json,'r')
            json_line = json.load(json_file)

            if element == JSON_START_DATE:
                json_line[JSON_START_DATE] = value[0]
            if element == JSON_END_DATE:
                json_line[JSON_END_DATE] = value[0]
            if element == JSON_PROFILE:
                json_line[JSON_PROFILE] =  value[0]
            if element == JSON_MODE:
                json_line[JSON_MODE] = value[0]
            if element == JSON_SHA256:
                json_line[JSON_SHA256_HASH] = value[0]
            if element == JSON_TEST_EXEC:
                json_line[JSON_TEST_EXEC] = {}
            if element == JSON_TEST_NAME:
                json_line[JSON_TEST_EXEC][value[0]] = []
            if element == JSON_TESTC:
                json_line[JSON_TEST_EXEC][value[0]].append({'order_exec':value[9], 'method':value[1], 'parameters':value[8], 'start_date':value[2], 'end_date':value[3], 'method_mode':value[4], 'concurrency_inst':value[5], 'exit_status':value[6], 'exit_msg':value[7]})
            if element == JSON_EXIT_ST:
                json_line[JSON_EXIT_ST] = value[0]
            if element == JSON_EXIT_MSG:
                json_line[JSON_EXIT_MSG] = value[0]
            if element == JSON_CHKSUM:
                json_line[JSON_SHA256] = value[0]

            json_file.close()

            with open(self.test_json, 'w') as json_file:
                json.dump(json_line, json_file, indent =2)

        os.remove(lock_pathfile)


    def initJSON(self):
        """
        Write msg in log file.

        type: str
        @param: element - element name

        type: list
        @param: value - list with nested values for element
        """

        json_file = open(self.test_json,'a')
        json_file.write('{')
        json_file.write('}')
        json_file.close()
